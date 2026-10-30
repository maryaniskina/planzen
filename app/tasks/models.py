from datetime import date, datetime, UTC
from enum import StrEnum

from beanie import Document
from pydantic import AwareDatetime, Field, model_validator, ValidationError


class TaskPriority(StrEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'


class TaskDocument(Document):
    title: str = Field(min_length=1, max_length=100)
    desc: str | None = None
    priority: TaskPriority = TaskPriority.LOW
    due_datetime: AwareDatetime | None = None
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    @model_validator(mode='after')
    def validate_due(self) -> 'TaskDocument':
        if self.due_date is not None and self.due_datetime is not None:
            raise ValidationError(
                'Нельзя передавать due_date и due_datetime вместе'
            )
        return self

    class Settings:
        name = 'tasks'
