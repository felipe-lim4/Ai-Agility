from datetime import datetime, timezone
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from domain.entities.enum.interaction_status import InteractionStatus
from domain.entities.readme_entity import ReadmeData
from domain.entities.tag_entity import TagData
from infra.database.models.readme_model import ReadmeModel
from infra.database.models.tag_model import TagModel


class SQLAlchemyReadmeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_readme_model(self, id: int) -> ReadmeModel | None:
        result = await self.db.execute(
            select(ReadmeModel)
            .options(selectinload(ReadmeModel.tags))
            .where(ReadmeModel.id == id)
        )
        return result.scalar_one_or_none()

    def _to_entity(self, model: ReadmeModel) -> ReadmeData:
        return ReadmeData(
            link_origin=model.link_origin,
            project_name=model.project_name,
            summary=model.summary,
            description=model.description,
            tree=model.tree,
            technologies=model.technologies,
            features=model.features,
            setup=model.setup,
            usage=model.usage,
            important_notes=model.important_notes,
            links=model.links,
            tags=[
                TagData(
                    id=tag.id,
                    name=tag.name,
                    description=tag.description,
                )
                for tag in model.tags
            ],
            status=model.status,
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def _get_existing_tags(self, tags: list[TagData | dict[str, Any]]) -> list[TagModel]:
        if not tags:
            return []

        tag_ids: set[int] = set()
        tag_names: set[str] = set()

        for tag in tags:
            if isinstance(tag, dict):
                tag_id = tag.get("id")
                tag_name = tag.get("name")
            else:
                tag_id = tag.id
                tag_name = tag.name

            if tag_id is not None:
                tag_ids.add(tag_id)
            if tag_name:
                tag_names.add(tag_name)

        filters = []
        if tag_ids:
            filters.append(TagModel.id.in_(tag_ids))
        if tag_names:
            filters.append(TagModel.name.in_(tag_names))

        if not filters:
            return []

        result = await self.db.execute(select(TagModel).where(or_(*filters)))
        return list(result.scalars().all())

    async def save(self, link_origin: str) -> int:
        model = ReadmeModel(
            link_origin=link_origin,
            status=InteractionStatus.SENT,
        )

        self.db.add(model)
        await self.db.flush()
        await self.db.commit()
        return model.id

    async def list_all(self) -> list[ReadmeData]:
        result = await self.db.execute(
            select(ReadmeModel).options(selectinload(ReadmeModel.tags))
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_id(self, id:int) -> ReadmeData | None:
        model = await self._get_readme_model(id)
        if not model:
            return None
        return self._to_entity(model)

    async def get_by_tag(self, tag_id: int) -> list[ReadmeData]:
        result = await self.db.execute(
            select(ReadmeModel)
            .join(ReadmeModel.tags)
            .options(selectinload(ReadmeModel.tags))
            .where(TagModel.id == tag_id)
        )
        models = result.scalars().unique().all()
        return [self._to_entity(model) for model in models]

    async def update(self, id: int, data: dict[str, Any]) -> ReadmeData | None:
        allowed_fields = {
            "link_origin",
            "project_name",
            "summary",
            "description",
            "tree",
            "technologies",
            "features",
            "setup",
            "usage",
            "important_notes",
            "links",
            "status",
            "tags",
        }

        update_data = {key: value for key, value in data.items() if key in allowed_fields}

        if not update_data:
            raise ValueError("No valid fields provided for update.")

        model = await self._get_readme_model(id)

        if model is None:
            return None

        if "tags" in update_data:
            model.tags = await self._get_existing_tags(update_data.pop("tags") or [])

        for key, value in update_data.items():
            setattr(model, key, value)

        model.updated_at = datetime.now(timezone.utc)

        await self.db.commit()

        self.db.expire_all()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        model = await self._get_readme_model(id)

        if model is None:
            return False

        self.db.delete(model)
        await self.db.commit()
        return True
