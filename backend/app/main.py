from fastapi import FastAPI

from app.api.endpoints import users
from app.api.endpoints import health
from app.api.endpoints import tasks
from app.api.endpoints import categories
from app.api.endpoints import tags
from app.api.endpoints import prediction
from app.api.endpoints import auth
from app.api.endpoints import admin

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(health.router)

    app.include_router(auth.router)

    app.include_router(admin.router)

    app.include_router(users.router)

    app.include_router(tasks.router)

    app.include_router(categories.router)

    app.include_router(tags.router)

    app.include_router(prediction.router)

    return app

app = create_app()
