from typing import Protocol

from domain.entities.tag_entity import TagData


class ITagRepository(Protocol):
    async def list_all(self) -> list[TagData]: ...
    async def list_names(self) -> list[str]: ...
