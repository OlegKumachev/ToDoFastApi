from datetime import date, datetime

from pydantic import BaseModel


class TasksBase(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False
    due_date: date | None = None
    created_at: datetime | None = None


class TaskCreate(TasksBase):
    pass


class Task(TasksBase):
    id: int
