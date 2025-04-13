from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException

from app.crud import (
    create_task_in_db,
    delete_task,
    get_task_id,
    get_tasks_by_status_or_date,
    get_tasks_from_db,
    update_task_in_db,
)
from app.schemas import Task, TaskCreate, TasksBase

router = APIRouter()


@router.post("/tasks/", response_model=Task, tags=["Создание задачи"])
async def create_task(task: Annotated[TaskCreate, Depends()]):
    try:
        return await create_task_in_db(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/", response_model=list[Task], tags=["Получение данных"])
async def get_tasks():
    try:
        tasks = await get_tasks_from_db()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/{id}", response_model=Task, tags=["Получение данных"])
async def get_task(task_id: int):
    try:
        task = await get_task_id(task_id)

        if task:
            return Task(**task)
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.get(
    "/tasks/search/", response_model=List[Task], tags=["Получение данных"]
)
async def search_tasks(
    is_completed: Optional[bool] = None,
    order: str = "asc",
):
    try:
        tasks = await get_tasks_by_status_or_date(
            is_completed=is_completed,
            order=order,
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.put("/tasks/{id}", tags=["Обновлние данных"])
async def update_task(task_id: int, task: Annotated[TasksBase, Depends()]):
    try:
        upd_task = await update_task_in_db(
            task_id=task_id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            is_completed=task.is_completed,
        )

        return upd_task

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )


@router.delete("/tasks/{id}", response_model=dict, tags=["Удаление задачи"])
async def remove_task(task_id: int):
    deleted_task = await delete_task(task_id)

    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": f"Task {task_id} deleted successfully"}
