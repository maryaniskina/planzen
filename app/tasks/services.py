from beanie import PydanticObjectId

from app.tasks.models import TaskDocument
from app.tasks.repositories import TaskRepository
from app.tasks.schemas import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    pass


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def create(self, data: TaskCreate) -> TaskDocument:
        task = TaskDocument(**data.model_dump())
        return await self.repository.create(task)

    async def get_by_id(self, task_id: PydanticObjectId) -> TaskDocument:
        task = await self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f'Задача с id {task_id} не найдена')
        return task

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TaskDocument]:
        if skip < 0:
            raise ValueError('skip не может быть отрицательным')
        if not 1 <= limit <= 100:
            raise ValueError('limit должен быть от 1 до 100')
        return await self.repository.get_all(skip=skip, limit=limit)

    async def update(
        self,
        task_id: PydanticObjectId,
        data: TaskUpdate,
    ) -> TaskDocument:
        task = await self.get_by_id(task_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            return task

        resulting_due_dt = update_data.get('due_datetime', task.due_datetime)
        resulting_due_date = update_data.get('due_date', task.due_date)
        if resulting_due_dt is not None and resulting_due_date is not None:
            raise ValueError(
                'Нельзя одновременно указать due_date и due_at'
            )
        return await self.repository.update(task, update_data)

    async def delete(self, task_id: PydanticObjectId) -> None:
        task = await self.get_by_id(task_id)
        await self.repository.delete(task)
