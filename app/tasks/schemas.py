from datetime import date

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

from app.tasks.models import TaskPriority


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    title: str = Field(min_length=1, max_length=100)
    desc: str | None = None
    priority: TaskPriority = TaskPriority.LOW
    due_datetime: AwareDatetime | None = None
    due_date: date | None = None

    @model_validator(mode='after')
    def validate_due(self) -> 'TaskCreate':
        if self.due_date is not None and self.due_datetime is not None:
            raise ValueError(
                'Нельзя передавать due_date и due_datetime вместе'
            )
        return self


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=100)
    desc: str | None = None
    priority: TaskPriority | None = None
    due_datetime: AwareDatetime | None = None
    due_date: date | None = None

    @model_validator(mode='after')
    def validate_title(self) -> 'TaskUpdate':
        if 'title' in self.model_fields_set and self.title is None:
            raise ValueError('Название задачи не может быть пустым')
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    desc: str | None
    priority: TaskPriority
    due_datetime: AwareDatetime | None
    due_date: date | None
