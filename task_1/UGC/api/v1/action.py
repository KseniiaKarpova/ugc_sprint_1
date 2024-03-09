from uuid import UUID

from aiokafka import AIOKafkaProducer
from core.config import settings
from core.handlers import JwtHandler, require_access_token
from db.kafka import get_kafka
from exceptions import success
from fastapi import APIRouter, Depends
from schemas.action import UserAction

router = APIRouter()


@router.post('/')
async def create_action(
    action: str,
    film_id: UUID,
    producer: AIOKafkaProducer = Depends(get_kafka),
    jwt_handler: JwtHandler = Depends(require_access_token)
):
    user = await jwt_handler.get_current_user()
    data = UserAction(
        action=action,
        user_id=str(user.uuid),
        film_id=film_id,
        ).model_dump_json().encode('utf-8')
    await producer.send(topic=settings.kafka.topic, value=data)
    return success
