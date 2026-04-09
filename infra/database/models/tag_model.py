from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from infra.database.models.base import BaseModel
from infra.database.models.readme_tag_model import readme_tag_table


class TagModel(BaseModel):
    __tablename__ = "tag"

    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=False)
    readmes = relationship("ReadmeModel", secondary=readme_tag_table, back_populates="tags")

