from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.tag_entity import TagData
from infra.database.models.tag_model import TagModel


class SQLAlchemyTagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[TagData]:
        result = await self.db.execute(select(TagModel))
        return [
            TagData(id=m.id, name=m.name, description=m.description)
            for m in result.scalars().all()
        ]

    async def list_names(self) -> list[str]:
        result = await self.db.execute(select(TagModel.name))
        return [row[0] for row in result.all()]
