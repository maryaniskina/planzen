from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.tasks.repositories import TaskRepository
from app.tasks.schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.tasks.services import (
    TaskNotFoundError,
    TaskService,
)

router = APIRouter(prefix='/tasks', tags=['Tasks'])


def get_task_service() -> TaskService:
    return TaskService(repository=TaskRepository())


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.post(
    '/',
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskCreate,
    service: TaskServiceDep,
):
    task = await service.create(data)
    return TaskResponse(
        id=str(task.id),
        **task.model_dump(exclude={'id'}),
    )


@router.get('/',response_model=list[TaskResponse])
async def get_tasks(
    service: TaskServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    tasks = await service.get_all(skip=skip, limit=limit)
    return [
        TaskResponse(
            id=str(task.id),
            **task.model_dump(exclude={'id'}),
        )
        for task in tasks
    ]


@router.get('/{task_id}', response_model=TaskResponse)
async def get_task(
    task_id: PydanticObjectId,
    service: TaskServiceDep,
):
    try:
        task = await service.get_by_id(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return TaskResponse(
        id=str(task.id),
        **task.model_dump(exclude={'id'}),
    )


@router.patch('/{task_id}', response_model=TaskResponse)
async def update_task(
    task_id: PydanticObjectId,
    data: TaskUpdate,
    service: TaskServiceDep,
):
    try:
        task = await service.update(task_id, data)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return TaskResponse(
        id=str(task.id),
        **task.model_dump(exclude={'id'}),
    )


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: PydanticObjectId,
    service: TaskServiceDep,
) -> None:
    try:
        await service.delete(task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
