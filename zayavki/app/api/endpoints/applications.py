from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from zayavki.app.core.database import async_session
from zayavki.app.db.repositories.application_repo import ApplicationRepository
from zayavki.app.core.kafka import producer
from zayavki.app.core.config import settings

application_router = APIRouter()


async def get_db():
    async with async_session() as session:
        yield session


@application_router.post("/")
async def create_application(
        user_name: str, description: str, db: AsyncSession = Depends(get_db)
):
    repo = ApplicationRepository(db)
    application = await repo.create_application(user_name, description)

    # Публикация события в Kafka
    message = {
        "id": application.id,
        "user_name": application.user_name,
        "description": application.description,
        "created_at": str(application.created_at)
    }
    await producer.send_and_wait(settings.KAFKA_TOPIC, value=message)

    return application


@application_router.get("/")
async def list_applications(
        user_name: str | None = Query(None),
        page: int = Query(1, gt=0),
        size: int = Query(10, gt=0),
        db: AsyncSession = Depends(get_db)
):
    skip = (page - 1) * size
    repo = ApplicationRepository(db)
    applications = await repo.get_applications(user_name, skip, size)
    return applications