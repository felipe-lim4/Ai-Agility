from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from application.health import HealthUseCase
from infra.database.database import get_db_sqlite
from infra.database.repositories.health import SQLAlchemyHealthRepository


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    timestamp: datetime


class DBHealthResponse(BaseModel):
    status: str 
    database: str


def get_health_repo_sqlite(db: AsyncSession = Depends(get_db_sqlite)) -> SQLAlchemyHealthRepository:
    return SQLAlchemyHealthRepository(db)


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
async def health(repo: SQLAlchemyHealthRepository = Depends(get_health_repo_sqlite)) -> HealthResponse:
    result = await HealthUseCase(repo).get_health()
    return HealthResponse(
        status=result.status,
        app_name=result.app_name,
        version=result.version,
        timestamp=result.timestamp,
    )


@router.get("/db-sqlite", response_model=DBHealthResponse)
async def health_db_sqlite(repo: SQLAlchemyHealthRepository = Depends(get_health_repo_sqlite)) -> DBHealthResponse:
    result = await HealthUseCase(repo).get_db_sqlite_health()
    return DBHealthResponse(status=result.status, database=result.database)