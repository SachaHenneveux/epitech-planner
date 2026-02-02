"""Credit Strategy Tool - Epitech Timeline Generator."""

__version__ = "1.0.0"
__author__ = "Sacha Henneveux"

from .models import Module, Activity, UserInfo
from .api import EpitechAPI
from .excel import generate_excel

__all__ = ["Module", "Activity", "UserInfo", "EpitechAPI", "generate_excel"]
