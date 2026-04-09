from sqlalchemy import JSON, Column, Enum, String
from sqlalchemy.orm import relationship
from domain.entities.enum.interaction_status import InteractionStatus
from infra.database.models.base import BaseModel
from infra.database.models.readme_tag_model import readme_tag_table



class ReadmeModel(BaseModel):
    __tablename__ = "readme"

    link_origin = Column(String, index=True, nullable=False)
    project_name = Column(String, index=True)
    summary = Column(String, index=True)
    description = Column(String, index=True)
    technologies = Column(JSON, nullable=False, default=list)
    features = Column(JSON, nullable=False, default=list)
    setup = Column(JSON, nullable=False, default=dict)
    usage = Column(JSON, nullable=False, default=dict)
    important_notes = Column(JSON, nullable=False, default=list)
    links = Column(JSON, nullable=False, default=list)
    tags = relationship("TagModel", secondary=readme_tag_table, back_populates="readmes")
    status = Column(Enum(InteractionStatus), index=True)


