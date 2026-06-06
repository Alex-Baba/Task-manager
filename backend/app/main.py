from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import users
from app.api.endpoints import health
from app.api.endpoints import tasks
from app.api.endpoints import categories
from app.api.endpoints import tags
from app.api.endpoints import predictions
from app.api.endpoints import auth
from app.api.endpoints import admin
from app.core import get_config


def create_app() -> FastAPI:
    app = FastAPI()
    config = get_config()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)

    app.include_router(auth.router)

    app.include_router(admin.router)

    app.include_router(users.router)

    app.include_router(tasks.router)

    app.include_router(categories.router)

    app.include_router(tags.router)

    app.include_router(predictions.router)

    return app


app = create_app()
