
from typing import Protocol

from domain.entities.readme_entity import ReadmeData


class IReadmeProcessRepository(Protocol):
    async def extract_repository_texts(self, link_origin: str) -> list[dict[str, str]]: ...
    async def get_response(self, link_origin: str, files: list[dict[str, str]]) -> ReadmeData: ...
