from datetime import date

from beanie import PydanticObjectId

from app.tasks.models import TaskDocument


class TaskRepository:

    async def create(self, task: TaskDocument) -> TaskDocument:
        return await task.insert()

    async def get_by_id(
        self,
        task_id: PydanticObjectId,
    ) -> TaskDocument | None:
        return await TaskDocument.get(task_id)

    async def get_all(
        self, 
        skip: int = 0, 
        limit: int = 50,
    ) -> list[TaskDocument]:
        pipeline = [
            {
                '$addFields': {
                    'sort_deadline': {
                        '$ifNull': ['$due_at', '$due_date'],
                    },
                },
            },
            {
                '$sort': {
                    'sort_deadline': 1,
                    '_id': 1,
                },
            },
            {'$skip': skip},
            {'$limit': limit},
            {'$unset': 'sort_deadline'},
        ]
        return await TaskDocument.aggregate(
            pipeline,
            projection_model=TaskDocument,
        ).to_list()

    async def update(
        self,
        task: TaskDocument,
        update_data: dict,
    ) -> TaskDocument:
        for field, value in update_data.items():
            setattr(task, field, value)
        await task.save()
        return task

    async def delete(self, task: TaskDocument) -> None:
        await task.delete()
