from datetime import datetime

from pydantic import BaseModel

from domain.entities.enum.interaction_status import InteractionStatus


class GenerateReadmeRequest(BaseModel):
    link_origin: str


class GenerateReadmeResponse(BaseModel):
    id: int


class DeleteReadmeResponse(BaseModel):
    success: bool


class TagPayload(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None


class TagResponse(BaseModel):
    id: int | None = None
    name: str
    description: str


class ReadmeResponse(BaseModel):
    id: int | None = None
    link_origin: str
    project_name: str | None = None
    summary: str | None = None
    description: str | None = None
    technologies: list[str]
    features: list[str]
    setup: dict
    usage: dict
    important_notes: list[str]
    links: list[str]
    status: InteractionStatus
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tags: list[TagResponse]


class UpdateReadmeRequest(BaseModel):
    link_origin: str | None = None
    project_name: str | None = None
    summary: str | None = None
    description: str | None = None
    technologies: list[str] | None = None
    features: list[str] | None = None
    setup: dict | None = None
    usage: dict | None = None
    important_notes: list[str] | None = None
    links: list[str] | None = None
    status: InteractionStatus | None = None
    tags: list[TagPayload] | None = None