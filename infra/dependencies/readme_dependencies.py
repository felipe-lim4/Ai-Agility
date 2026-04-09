from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.readme.readme_usecase import (
    DeleteReadmeUseCase,
    GenerateReadmeUseCase,
    GetReadmeByIdUseCase,
    GetReadmesByTagUseCase,
    ListDocumentsUseCase,
    UpdateReadmeUseCase,
)
from domain.repositories.readme_process_repository import IReadmeProcessRepository
from infra.azure_services.readme_process_repository import AzureReadmeProcessRepository
from infra.database.database import get_db_sqlite
from infra.database.repositories.readme_persistence import SQLAlchemyReadmeRepository


def get_readme_repository(db: AsyncSession = Depends(get_db_sqlite)) -> SQLAlchemyReadmeRepository:
    return SQLAlchemyReadmeRepository(db)



def get_readme_process_repository() -> IReadmeProcessRepository:
    return AzureReadmeProcessRepository()


def get_generate_readme_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
    process_repo: IReadmeProcessRepository = Depends(get_readme_process_repository),
) -> GenerateReadmeUseCase:
    return GenerateReadmeUseCase(repo, process_repo)


def get_readme_by_id_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
) -> GetReadmeByIdUseCase:
    return GetReadmeByIdUseCase(repo)


def get_list_documents_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
) -> ListDocumentsUseCase:
    return ListDocumentsUseCase(repo)


def get_readmes_by_tag_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
) -> GetReadmesByTagUseCase:
    return GetReadmesByTagUseCase(repo)


def get_update_readme_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
) -> UpdateReadmeUseCase:
    return UpdateReadmeUseCase(repo)


def get_delete_readme_use_case(
    repo: SQLAlchemyReadmeRepository = Depends(get_readme_repository),
) -> DeleteReadmeUseCase:
    return DeleteReadmeUseCase(repo)
