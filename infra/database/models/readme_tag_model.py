from sqlalchemy import Column, ForeignKey, Table

from infra.database.models.base import Base


readme_tag_table = Table(
    "readme_tag",
    Base.metadata,
    Column("readme_id", ForeignKey("readme.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)