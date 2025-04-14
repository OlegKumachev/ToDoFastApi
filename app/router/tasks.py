from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends

from app.schemas.tasks import Task, TaskCreate, TasksBase
from app.services.task import (
    create_task_service,
    get_task_id_service,
    get_tasks_service,
    remove_task_service,
    task_search_service,
    update_task_service,
)

router = APIRouter()


@router.post("/tasks/", response_model=Task, tags=["Создание задачи"])
async def create_task_route(task: Annotated[TaskCreate, Depends()]):
    return await create_task_service(task)


@router.get("/tasks/", response_model=list[Task], tags=["Получение данных"])
async def get_tasks_route():
    return await get_tasks_service()


@router.get("/tasks/{id}", response_model=Task, tags=["Получение данных"])
async def get_task_route(task_id: int):
    return await get_task_id_service(task_id)


@router.get(
    "/tasks/search/", response_model=List[Task], tags=["Получение данных"]
)
async def search_tasks_route(
    is_completed: Optional[bool] = None,
    order: str = "asc",
):
    return await task_search_service(is_completed=is_completed, order=order)


@router.put("/tasks/{id}", tags=["Обновление данных"])
async def update_task_route(
    task_id: int, task: Annotated[TasksBase, Depends()]
):
    return await update_task_service(task_id, task)


@router.delete("/tasks/{id}", response_model=dict, tags=["Удаление задачи"])
async def remove_task_route(task_id: int):
    return await remove_task_service(task_id)
