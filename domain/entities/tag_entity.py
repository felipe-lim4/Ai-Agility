from dataclasses import dataclass


@dataclass
class TagData:
    name: str
    description: str
    id: int | None = None