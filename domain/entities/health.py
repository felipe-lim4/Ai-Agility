
from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealthStatus:
    status: str
    app_name: str
    version: str
    timestamp: datetime


@dataclass
class DBHealthStatus:
    status: str
    database: str