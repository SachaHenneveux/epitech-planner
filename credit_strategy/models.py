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
    student_credits: int = 0  # Credits earned (0 = pending if registered)


@dataclass
class UserInfo:
    """User profile information from Epitech intranet."""

    login: str
    name: str
    semester: int
    student_year: int
    promo: int
    credits: int  # Total validated credits
    gpa: float
