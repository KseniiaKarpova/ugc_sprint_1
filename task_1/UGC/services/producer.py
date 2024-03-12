from functools import lru_cache
from uuid import UUID
from fastapi import Depends
from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka
from schemas.action import UserAction
from utils.jaeger import TraceAction
from schemas.auth import JWTUserData
from core.config import settings
from exceptions import success
from datetime import datetime
from opentelemetry import trace

class ProducerService:
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    @TraceAction('create_action_execution')
    async def produce(self, user: JWTUserData, film_id: UUID, action: str):
        data = UserAction(
            action=action,
            user_id=str(user.uuid),
            film_id=str(film_id),
            created_at=datetime.utcnow()
            ).model_dump_json().encode('utf-8')
        await self.producer.send(topic=settings.kafka.topic, value=data)
        return success


@lru_cache()
def get_producer_service(
    producer: AIOKafkaProducer = Depends(get_kafka),
    ):
    return ProducerService(producer=producer)
