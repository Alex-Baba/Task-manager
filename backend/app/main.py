from fastapi import FastAPI

from app.api.endpoints import users
from app.api.endpoints import health

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(health.router)

    app.include_router(users.router)

    return app

app = create_app()