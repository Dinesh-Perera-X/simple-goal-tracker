from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GoalCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title is required")
        return value


class GoalUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=False)

    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Title is required")
        return value


class Goal(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().hex)
    title: str
    description: str = ""
    completed: bool = False
