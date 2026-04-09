from typing import Protocol
from domain.entities.health import DBHealthStatus, HealthStatus


class IHealthRepository(Protocol):
    async def get_status(self) -> HealthStatus: ...
    async def get_db_sqlite_status(self) -> DBHealthStatus: ...
