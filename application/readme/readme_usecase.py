from typing import Any

from domain.entities.enum.interaction_status import InteractionStatus
from domain.entities.readme_entity import ReadmeData
from domain.repositories.readme_process_repository import IReadmeProcessRepository
from domain.repositories.readme_repository import IReadmeRepository
from domain.repositories.tag_repository import ITagRepository
from infra.core.config import settings

logger = settings.logger



class GenerateReadmeUseCase:
    def __init__(self, readme_repository: IReadmeRepository, readme_process_repository: IReadmeProcessRepository, tag_repository: ITagRepository) -> None:
        self.readme_repository = readme_repository
        self.readme_process_repository = readme_process_repository
        self.tag_repository = tag_repository

    @staticmethod
    def _to_update_data(readme: ReadmeData) -> dict[str, Any]:
        return {
            "link_origin": readme.link_origin,
            "project_name": readme.project_name,
            "summary": readme.summary,
            "description": readme.description,
            "tree": readme.tree,
            "technologies": readme.technologies,
            "features": readme.features,
            "setup": readme.setup,
            "usage": readme.usage,
            "important_notes": readme.important_notes,
            "links": readme.links,
            "status": readme.status,
            "tags": [
                {"id": tag.id, "name": tag.name, "description": tag.description}
                for tag in readme.tags
            ],
        }

    async def execute(self, link_origin: str) -> int:
        logger.info("[GenerateReadme] Starting for: %s", link_origin)
        readme_id = await self.readme_repository.save(link_origin)
        logger.info("[GenerateReadme] Created readme record id=%d, setting PROCESSING", readme_id)
        await self.readme_repository.update(readme_id, {"status": InteractionStatus.PROCESSING})

        try:
            logger.info("[GenerateReadme] Extracting repository texts...")
            repo_data = await self.readme_process_repository.extract_repository_texts(link_origin)
            logger.info("[GenerateReadme] Extracted %d files, calling LLM...", len(repo_data["files"]))
            available_tags = await self.tag_repository.list_names()
            generated_readme = await self.readme_process_repository.get_response(link_origin, repo_data, available_tags)
            generated_readme.status = InteractionStatus.FINISHED
            logger.info("[GenerateReadme] LLM succeeded, updating record id=%d to FINISHED", readme_id)
            await self.readme_repository.update(readme_id, self._to_update_data(generated_readme))
        except Exception:
            logger.exception("[GenerateReadme] Error processing readme id=%d", readme_id)
            await self.readme_repository.update(readme_id, {"status": InteractionStatus.ERROR})
            raise

        logger.info("[GenerateReadme] Completed successfully, id=%d", readme_id)
        return readme_id

   
class GetReadmeByIdUseCase:
    def __init__(self, readme_repository: IReadmeRepository) -> None:
        self.readme_repository = readme_repository

    async def execute(self, id: int) -> ReadmeData | None:
        return await self.readme_repository.get_by_id(id)


class ListDocumentsUseCase:
    def __init__(self, readme_repository: IReadmeRepository) -> None:
        self.readme_repository = readme_repository

    async def execute(self) -> list[ReadmeData]:
        return await self.readme_repository.list_all()


class GetReadmesByTagUseCase:
    def __init__(self, readme_repository: IReadmeRepository) -> None:
        self.readme_repository = readme_repository

    async def execute(self, tag_id: int) -> list[ReadmeData]:
        return await self.readme_repository.get_by_tag(tag_id)


class UpdateReadmeUseCase:
    def __init__(self, readme_repository: IReadmeRepository) -> None:
        self.readme_repository = readme_repository

    async def execute(self, id: int, data: dict[str, Any]) -> ReadmeData | None:
        return await self.readme_repository.update(id, data)


class DeleteReadmeUseCase:
    def __init__(self, readme_repository: IReadmeRepository) -> None:
        self.readme_repository = readme_repository

    async def execute(self, id: int) -> bool:
        return await self.readme_repository.delete(id)


class ListTagsUseCase:
    def __init__(self, tag_repository: ITagRepository) -> None:
        self.tag_repository = tag_repository

    async def execute(self) -> list:
        return await self.tag_repository.list_all()