from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException

from app.database import get_db
from app.schemas import Task


async def create_task_in_db(
    title: str,
    description: str = None,
    due_date: date = None,
):
    async with get_db() as conn:
        try:
            result = await conn.fetchrow(
                "INSERT INTO tasks (title, description, due_date, created_at) VALUES ($1, $2, $3, NOW()) RETURNING id",
                title,
                description,
                due_date,
            )
            return {
                "id": result["id"],
                "title": title,
                "description": description,
                "due_date": due_date,
                "is_completed": False,
                "created_at": datetime.now(),
            }

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


async def get_tasks_from_db():
    async with get_db() as conn:
        tasks = await conn.fetch(
            """
                                 SELECT
                                 id,
                                 title,
                                 description,
                                 due_date,
                                 is_completed,
                                 created_at
                                 FROM tasks
                                 ORDER BY created_at DESC
                            """,
        )
        return [Task(**task) for task in tasks]


async def get_task_id(task_id: int):
    async with get_db() as conn:

        query = await conn.fetchrow(
            """
                SELECT id,
                title,
                description,
                due_date,
                is_completed,
                created_at
                FROM tasks
                WHERE id = $1;
            """,
            task_id,
        )

        return query


async def update_task_in_db(
    task_id: int,
    title: str,
    description: str,
    due_date: date,
    is_completed: bool,
):
    async with get_db() as conn:
        current_task = await conn.fetchrow(
            "SELECT * FROM tasks WHERE id = $1",
            task_id,
        )
        if not current_task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        updated_task = await conn.fetchrow(
            """
            UPDATE tasks
            SET title = $1,
                description = $2,
                due_date = $3,
                is_completed = $4
            WHERE id = $5
            RETURNING *;
        """,
            title,
            description,
            due_date,
            is_completed,
            task_id,
        )

        return updated_task


async def delete_task(task_id: int):
    async with get_db() as conn:

        result = await conn.fetchrow(
            """
            DELETE FROM tasks WHERE id = $1 RETURNING id;
            """,
            task_id,
        )

    return result


async def get_tasks_by_status_or_date(
    is_completed: Optional[bool] = None,
    due_date: Optional[str] = None,
    order: str = "asc",
):

    async with get_db() as conn:
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        param_index = 1

        if is_completed is not None:
            query += f" AND is_completed = ${param_index}"
            params.append(is_completed)
            param_index += 1

        if order not in ["asc", "desc"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid order parameter. Use 'asc' or 'desc'.",
            )

        if due_date is not None:
            query += f" AND due_date = ${param_index}"
            params.append(due_date)
            param_index += 1

        query += f" ORDER BY created_at {order}"

        tasks = await conn.fetch(query, *params)
        return [Task(**task) for task in tasks]
