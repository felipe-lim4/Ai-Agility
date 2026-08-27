from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.health import DBHealthStatus, HealthStatus
from infra.core.config import settings



class SQLAlchemyHealthRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._logger = settings.logger

    async def get_status(self) -> HealthStatus:
        return HealthStatus(
            status="healthy",
            app_name="ai-agility",
            version="dev",
            timestamp=datetime.now(timezone.utc),
        )

    async def get_db_sqlite_status(self) -> DBHealthStatus:
        try:
            await self._db.execute(text("SELECT 1"))
            return DBHealthStatus(status="healthy", database="sqlite")
        except Exception as e:
            self._logger.error("[health] SQLite unhealthy: %s", e, exc_info=True)
            return DBHealthStatus(status="unhealthy", database="sqlite")