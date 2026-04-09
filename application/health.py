from domain.entities.health import DBHealthStatus, HealthStatus
from domain.repositories.health import IHealthRepository


class HealthUseCase:
    def __init__(self, repo: IHealthRepository) -> None:
        self._repo = repo

    async def get_health(self) -> HealthStatus:
        return await self._repo.get_status()

    async def get_db_sqlite_health(self) -> DBHealthStatus:
        return await self._repo.get_db_sqlite_status()

    # async def get_db_postgres_health(self) -> DBHealthStatus:
    #     return await self._repo.get_db_postgres_status()
