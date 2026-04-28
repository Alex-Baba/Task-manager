from fastapi import FastAPI

from app.api.endpoints import users
from app.api.endpoints import health
from app.api.endpoints import tasks
from app.api.endpoints import categories

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(health.router)

    app.include_router(users.router)

    app.include_router(tasks.router)

    app.include_router(categories.router)

    return app

app = create_app()