
from typing import Protocol

from domain.entities.readme_entity import ReadmeData


class IReadmeProcessRepository(Protocol):
    async def extract_repository_texts(self, link_origin: str) -> dict: ...
    async def get_response(self, link_origin: str, repo_data: dict) -> ReadmeData: ...
