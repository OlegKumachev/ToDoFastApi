from typing import List, Optional

from fastapi import HTTPException

from app.repositories.task import (
    create_task_in_db,
    filter_tasks_in_db,
    get_task_by_id,
    get_tasks,
    remove_task_on_db,
    update_task_in_db,
)
from app.schemas.tasks import Task, TaskCreate, TasksBase


async def create_task_service(task: TaskCreate) -> Task:
    try:
        return await create_task_in_db(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_tasks_service():
    try:
        tasks = await get_tasks()
        return [Task(**task) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def get_task_id_service(task_id: int) -> Task:
    try:
        task_data = await get_task_by_id(task_id)
        if task_data:
            return Task(**dict(task_data))
        else:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


async def task_search_service(
    is_completed: Optional[bool] = None, due_date=None, order: str = "asc"
) -> List[Task]:
    try:
        tasks = await filter_tasks_in_db(
            is_completed=is_completed,
            due_date=due_date,
            order=order,
        )
        return [Task(**task) for task in tasks]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


async def update_task_service(task_id: int, task: TasksBase) -> Task:
    try:
        upd_task = await update_task_in_db(
            task_id=task_id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            is_completed=task.is_completed,
        )
        return Task(**upd_task)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


async def remove_task_service(task_id: int):
    try:
        deleted_task = await remove_task_on_db(task_id)

        if deleted_task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        return {"message": f"Задача {task_id} удалена"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )
