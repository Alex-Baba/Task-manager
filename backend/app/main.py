from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated

from app.db.session import get_db

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db")
async def test_db(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(text("SELECT 1"))
    return {"status": "ok", "result": result.scalar()}