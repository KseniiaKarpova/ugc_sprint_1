import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import action
from core.config import settings
from core.logger import LOGGING
from db import kafka, redis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.kafka = AIOKafkaProducer(
        loop=asyncio.get_event_loop(),
        bootstrap_servers=f'{settings.kafka.host}:9092')
    redis.redis = Redis(host=settings.redis.host, port=settings.redis.port)
    await kafka.kafka.start()
    yield
    await kafka.kafka.stop()
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description="UGC - Сервис для хранения событий в Kafka",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(action.router, prefix='/api/v1/action', tags=['films'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
