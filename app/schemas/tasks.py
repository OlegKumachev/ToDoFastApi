from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class TasksBase(BaseModel):
    title: Annotated[
        str, Field(..., title="Название задачи", min_length=2, max_length=64)
    ]
    description: Annotated[
        Optional[str], Field(None, title="Полное описание задачи")
    ]
    is_completed: Annotated[bool, Field(default=False, title="Статус задачи")]
    due_date: Annotated[date, Field(..., title="Срок выполнения задачи")]
    created_at: Optional[datetime] = None


class TaskCreate(TasksBase):
    pass


class Task(TasksBase):
    id: Annotated[
        int,
        Field(
            ...,
        ),
    ]
