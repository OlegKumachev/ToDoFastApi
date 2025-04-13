from contextlib import asynccontextmanager

import asyncpg
from environs import Env
from fastapi import FastAPI

env = Env()
env.read_env()

DATABASE_URL = env("DATABASE_URL")


@asynccontextmanager
async def get_db():
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        yield conn
    await pool.close()


async def connect_to_db(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)
    await init_db(app)


async def init_db(app: FastAPI):
    async with app.state.pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due_date DATE,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """,
        )


async def disconnect_from_db(app: FastAPI):
    await app.state.pool.close()
