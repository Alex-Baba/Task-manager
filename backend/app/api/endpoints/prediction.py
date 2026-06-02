from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.session import get_session
from app.models.users import User
from app.schemas.common import Message
from app.schemas.task_predictions import PredictionApply, PredictionUpdate, TaskPredictionRead
from app.schemas.tasks import TaskRead
from app.services.prediction import PredictionService

router = APIRouter(
    prefix="/tasks/{task_id}/predictions",
    tags=["Predictions"],
)


@router.post(
    "/generate",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_201_CREATED,
)
async def generate_prediction(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.generate_prediction_for_task(
        user_id=current_user.id,
        task_id=task_id,
    )


@router.get(
    "/active",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_200_OK,
)
async def get_active_prediction(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.get_active_prediction_for_task(
        user_id=current_user.id,
        task_id=task_id,
    )


@router.get(
    "",
    response_model=list[TaskPredictionRead],
    status_code=status.HTTP_200_OK,
)
async def get_predictions(
    task_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TaskPredictionRead]:
    service = PredictionService(session)
    return await service.get_predictions_for_task(
        user_id=current_user.id,
        task_id=task_id,
    )


@router.patch(
    "/{prediction_id}",
    response_model=TaskPredictionRead,
    status_code=status.HTTP_200_OK,
)
async def update_prediction(
    task_id: UUID,
    prediction_id: UUID,
    payload: PredictionUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskPredictionRead:
    service = PredictionService(session)
    return await service.update_prediction(
        user_id=current_user.id,
        task_id=task_id,
        prediction_id=prediction_id,
        payload=payload,
    )


@router.post(
    "/{prediction_id}/apply",
    response_model=TaskRead,
    status_code=status.HTTP_200_OK,
)
async def apply_prediction(
    task_id: UUID,
    prediction_id: UUID,
    payload: PredictionApply,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRead:
    service = PredictionService(session)
    return await service.apply_prediction(
        user_id=current_user.id,
        task_id=task_id,
        prediction_id=prediction_id,
        payload=payload,
    )


@router.delete(
    "/{prediction_id}",
    response_model=Message,
    status_code=status.HTTP_200_OK,
)
async def delete_prediction(
    task_id: UUID,
    prediction_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Message:
    service = PredictionService(session)
    return await service.delete_prediction(
        user_id=current_user.id,
        task_id=task_id,
        prediction_id=prediction_id,
    )
