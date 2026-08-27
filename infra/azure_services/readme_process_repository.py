import asyncio
import json

from domain.entities.readme_entity import ReadmeData
from domain.entities.tag_entity import TagData
from domain.repositories.readme_process_repository import IReadmeProcessRepository
from infra.azure_services.llm_service import LLMService, StructuredInput
from infra.core.config import settings
from infra.core.load_prompts import build_prompt
from infra.utils.utils import extract_repository_code

logger = settings.logger

class AzureReadmeProcessRepository(IReadmeProcessRepository):
    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()

    @staticmethod
    def _parse_tag(raw_tag: object) -> TagData | None:
        if isinstance(raw_tag, str) and raw_tag.strip():
            return TagData(name=raw_tag.strip(), description="")

        if not isinstance(raw_tag, dict):
            return None

        name = raw_tag.get("name")
        if not isinstance(name, str) or not name.strip():
            return None

        description = raw_tag.get("description")
        return TagData(
            id=raw_tag.get("id"),
            name=name.strip(),
            description=description if isinstance(description, str) else "",
        )

    @classmethod
    def _parse_tags(cls, raw_tags: object) -> list[TagData]:
        if not isinstance(raw_tags, list):
            return []

        return [tag for item in raw_tags if (tag := cls._parse_tag(item)) is not None]

    @classmethod
    def _clean_response(cls, response: str) -> str:
         # Strip markdown code fences if present
        cleaned = response.strip()
        if cleaned.startswith("```"):
            first_newline = cleaned.find("\n")
            if first_newline != -1:
                cleaned = cleaned[first_newline + 1:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
        return cleaned

    async def extract_repository_texts(self, link_origin: str) -> dict:
        logger.info("[ProcessRepo] Cloning and extracting texts from: %s", link_origin)
        result = await asyncio.to_thread(extract_repository_code, link_origin)
        logger.info("[ProcessRepo] Extracted %d files, %d dependencies from repository",
                    len(result["files"]), len(result["dependencies"]))
        return result

    async def get_response(self, link_origin: str, repo_data: dict, available_tags: list[str] | None = None) -> ReadmeData:
        logger.info("[ProcessRepo] Building prompt and calling LLM for: %s", link_origin)
        prompts = build_prompt()
        prompt = prompts[0] if prompts else ""

        structured_input = StructuredInput(
            repo_url=link_origin,
            tree=repo_data["tree"],
            dependencies=repo_data["dependencies"],
            readme_original=repo_data.get("readme_original"),
            available_tags=available_tags or [],
            files=repo_data["files"],
        )

        response_text = await asyncio.to_thread(
            self.llm_service.get_response_from_azure_openai,
            prompt,
            structured_input,
        )
        logger.info("[ProcessRepo] LLM raw response:\n%s", response_text[:1000])

        response_text = self._clean_response(response_text)

        try:
            response_data = json.loads(response_text)
        except json.JSONDecodeError as exc:
            logger.error("[ProcessRepo] Failed to parse JSON after cleanup: %s", response_text[:500])
            raise ValueError("LLM response is not valid JSON.") from exc

        if not isinstance(response_data, dict):
            raise ValueError("LLM response must be a JSON object.")
        logger.debug("response data: %s", response_data)
        print("response data:", response_data)
        print("tags atribuidas", response_data.get("tags"))

        return ReadmeData(
            link_origin=link_origin,
            project_name=response_data.get("project_name"),
            summary=response_data.get("summary"),
            description=response_data.get("description"),
            tree=response_data.get("tree") or repo_data["tree"],
            technologies=response_data.get("technologies") if isinstance(response_data.get("technologies"), list) else [],
            features=response_data.get("features") if isinstance(response_data.get("features"), list) else [],
            setup=response_data.get("setup") if isinstance(response_data.get("setup"), dict) else {},
            usage=response_data.get("usage") if isinstance(response_data.get("usage"), dict) else {},
            important_notes=response_data.get("important_notes") if isinstance(response_data.get("important_notes"), list) else [],
            links=response_data.get("links") if isinstance(response_data.get("links"), list) else [],
            tags=self._parse_tags(response_data.get("tags")),
        )