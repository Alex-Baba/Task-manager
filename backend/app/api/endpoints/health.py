from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Annotated
from fastapi import APIRouter

from app.db.session import get_session


router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    return {"Hello": "App"}


@router.get("/test-db")
async def test_db(db: Annotated[AsyncSession, Depends(get_session)]):
    result = await db.execute(text("SELECT 1"))
    return {"status": "ok", "result": result.scalar()}
