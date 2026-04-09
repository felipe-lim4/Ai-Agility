from typing import AsyncGenerator

from sqlalchemy import select, text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from infra.database.models.tag_model import TagModel


engine = create_async_engine("sqlite+aiosqlite:///./db/persistent.db")
async_session_sqlite = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# postgres_url = URL.create(
#     drivername="postgresql+asyncpg",
#     username=settings.POSTGRES_USER,
#     password=settings.POSTGRES_PASSWORD,
#     host=settings.POSTGRES_HOST,
#     port=5432,
#     database=settings.POSTGRES_DB,
# )
# engine_postgres = create_async_engine(postgres_url, echo=True)

# async_session_postgres = async_sessionmaker(engine_postgres, class_=AsyncSession, expire_on_commit=False)


DEFAULT_TAGS = [
    {"name": "python", "description": "Projetos e automacoes em Python."},
    {"name": "java", "description": "Projetos e servicos desenvolvidos em Java."},
    {"name": "spring-boot", "description": "Aplicacoes e APIs construidas com Spring Boot."},
    {"name": "fastapi", "description": "APIs e servicos desenvolvidos com FastAPI."},
    {"name": "backend", "description": "Implementacoes focadas em regras de negocio e APIs."},
    {"name": "frontend", "description": "Interfaces web e experiencias de usuario."},
    {"name": "clean-architecture", "description": "Projetos organizados com principios de arquitetura limpa."},
    {"name": "database", "description": "Modelagem, persistencia e integracao com bancos de dados."},
    {"name": "ai", "description": "Integracoes com modelos de linguagem e recursos de IA."},
    {"name": "devops", "description": "Automacao, deploy e operacao de servicos."},
]


async def seed_default_tags() -> None:
    async with async_session_sqlite() as session:
        result = await session.execute(select(TagModel.id).limit(1))
        existing_tag = result.scalar_one_or_none()

        if existing_tag is not None:
            return

        session.add_all([TagModel(name=tag["name"], description=tag["description"]) for tag in DEFAULT_TAGS])
        await session.commit()


async def get_db_sqlite() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_sqlite() as session:
        yield session

# async def get_db_postgres() -> AsyncGenerator[AsyncSession, None]: 
#     async with async_session_postgres() as session:
#         yield session
