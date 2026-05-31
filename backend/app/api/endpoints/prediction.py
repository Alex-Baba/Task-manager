from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.common import Message
from app.schemas.task_predictions import PredictionUpdate, TaskPredictionRead
from app.services.prediction import PredictionService

router = APIRouter(
    prefix="/users/{user_id}/tasks/{task_id}/predictions",
    tags=["Predictions"],
)


@router.post(
    "/generate",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_201_CREATED,
)
async def generate_prediction(
    user_id: UUID,
    task_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.generate_prediction_for_task(
        user_id=user_id,
        task_id=task_id,
    )


@router.get(
    "/active",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_200_OK,
)
async def get_active_prediction(
    user_id: UUID,
    task_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.get_active_prediction_for_task(
        user_id=user_id,
        task_id=task_id,
    )


@router.get(
    "",
    response_model=list[TaskPredictionRead],
    status_code=status.HTTP_200_OK,
)
async def get_predictions(
    user_id: UUID,
    task_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TaskPredictionRead]:
    service = PredictionService(session)
    return await service.get_predictions_for_task(
        user_id=user_id,
        task_id=task_id,
    )


@router.patch(
    "/{prediction_id}",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_200_OK,
)
async def update_prediction(
    user_id: UUID,
    task_id: UUID,
    prediction_id: UUID,
    payload: PredictionUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.update_prediction(
        user_id=user_id,
        task_id=task_id,
        prediction_id=prediction_id,
        payload=payload,
    )


@router.post(
    "/{prediction_id}/activate",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_200_OK,
)
async def activate_prediction(
    user_id: UUID,
    task_id: UUID,
    prediction_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.activate_prediction(
        user_id=user_id,
        task_id=task_id,
        prediction_id=prediction_id,
    )


@router.delete(
    "/{prediction_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
)
async def delete_prediction(
    user_id: UUID,
    task_id: UUID,
    prediction_id: UUID,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = PredictionService(session)
    return await service.delete_prediction(
        user_id=user_id,
        task_id=task_id,
        prediction_id=prediction_id,
    )
