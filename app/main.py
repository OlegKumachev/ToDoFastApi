from fastapi import FastAPI

from app.database import connect_to_db, disconnect_from_db
from app.router import tasks

app = FastAPI()


@app.on_event("startup")
async def startup():
    await connect_to_db(app)


@app.on_event("shutdown")
async def shutdown():
    await disconnect_from_db(app)


app.include_router(tasks.router)
