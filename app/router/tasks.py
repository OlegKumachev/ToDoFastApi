from typing import List, Optional

from fastapi import APIRouter, HTTPException

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


@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    try:
        return await create_task_in_db(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/", response_model=list[Task])
async def get_tasks():
    try:
        tasks = await get_tasks_from_db()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks/{id}", response_model=Task)
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


@router.put("/tasks/{id}")
async def update_task(task_id: int, task: TasksBase):
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


@router.delete("/tasks/{id}", response_model=dict)
async def remove_task(task_id: int):
    deleted_task = await delete_task(task_id)

    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": f"Task {task_id} deleted successfully"}


@router.get("/tasks/search/", response_model=List[Task])
async def search_tasks(
    due_date: Optional[str] = None,
    is_completed: Optional[bool] = None,
    order: str = "asc",
):
    try:
        tasks = await get_tasks_by_status_or_date(
            due_date=due_date,
            is_completed=is_completed,
            order=order,
        )
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}",
        )
