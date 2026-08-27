from domain.entities.enum.interaction_status import InteractionStatus
from datetime import datetime
from dataclasses import dataclass, field
from domain.entities.tag_entity import TagData


@dataclass
class ReadmeData:
    link_origin: str
    project_name: str | None = None
    summary: str | None = None
    description: str | None = None
    tree: str | None = None
    technologies: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    setup: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    important_notes: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    status: InteractionStatus = InteractionStatus.SENT
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    tags: list[TagData] = field(default_factory=list)

