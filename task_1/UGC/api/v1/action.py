from fastapi import APIRouter, Depends
from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka
from uuid import UUID
from core.config import settings
from schemas.action import UserAction
from core.handlers import require_access_token, JwtHandler
from exceptions import success


router = APIRouter()

@router.post('/')
async def create_action(
    action: str,
    film_id: UUID,
    uuid: UUID,
    producer : AIOKafkaProducer = Depends(get_kafka),
    #jwt_handler: JwtHandler = Depends(require_access_token)
):
    #user = await jwt_handler.get_current_user()
    data = UserAction(
        action=action,
        user_id=str(uuid),
        film_id=film_id,
        ).model_dump_json().encode('utf-8')
    await producer.send(topic=settings.kafka.topic, value=data)
    return success
