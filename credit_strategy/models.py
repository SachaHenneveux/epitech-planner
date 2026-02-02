"""Data models for Epitech modules and activities."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Activity:
    """Represents a project/activity within a module."""

    title: str
    type_title: str
    begin: datetime
    end: datetime
    module_title: str


@dataclass
class Module:
    """Represents an Epitech module with its metadata and activities."""

    id: int
    code: str
    instance: str
    title: str
    credits: int
    semester: int
    begin: datetime | None
    end: datetime | None
    scolaryear: int
    activities: list[Activity] = field(default_factory=list)
    registered: bool = False
