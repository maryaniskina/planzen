
from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError

from app.database.mongodb import mongodb

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness_check() -> dict[str, str]:
    if mongodb.client is None:
        raise HTTPException(
            status_code=503,
            detail="MongoDB is not connected",
        )

    try:
        await mongodb.client.admin.command("ping")
    except PyMongoError as exc:
        raise HTTPException(
            status_code=503,
            detail="MongoDB is unavailable",
        ) from exc

    return {"status": "ready"}
