from datetime import date
from typing import Optional

from app.database import get_db


async def create_task_in_db(
    title: str, description: str = None, due_date: date = None
):
    async with get_db() as conn:
        result = await conn.fetchrow(
            """
            INSERT INTO tasks (title, description, due_date, created_at)
            VALUES ($1, $2, $3, NOW())
            RETURNING id, title, description, due_date, created_at;
        """,
            title,
            description,
            due_date,
        )

        return dict(result)  # Возвращаем полный набор данных с ID


async def get_tasks():
    async with get_db() as conn:
        return await conn.fetch(
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
        """
        )


async def get_task_by_id(task_id: int):
    async with get_db() as conn:
        return await conn.fetchrow(
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


async def update_task_in_db(
    task_id: int,
    title: str,
    description: str,
    due_date: date,
    is_completed: bool,
):
    async with get_db() as conn:
        return await conn.fetchrow(
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


async def remove_task_on_db(task_id: int):
    async with get_db() as conn:
        return await conn.fetchrow(
            """
            DELETE FROM tasks WHERE id = $1 RETURNING id;
            """,
            task_id,
        )


async def filter_tasks_in_db(
    is_completed: Optional[bool], due_date: Optional[str], order: str
):
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    param_index = 1

    if is_completed is not None:
        query += f" AND is_completed = ${param_index}"
        params.append(is_completed)
        param_index += 1

    if due_date is not None:
        query += f" AND due_date = ${param_index}"
        params.append(due_date)
        param_index += 1

    query += f" ORDER BY created_at {order}"

    async with get_db() as conn:
        return await conn.fetch(query, *params)
