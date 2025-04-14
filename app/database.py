from contextlib import asynccontextmanager

import asyncpg
from environs import Env
from fastapi import FastAPI

env = Env()
env.read_env()


@asynccontextmanager
async def get_db():
    conn = await asyncpg.connect(env("DATABASE_URL"))
    try:
        yield conn
    finally:
        await conn.close()


async def connect_to_db(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(env("DATABASE_URL"))
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
            """
        )


async def disconnect_from_db(app: FastAPI):
    await app.state.pool.close()
