import logging
from contextlib import asynccontextmanager
from functools import lru_cache
import uvicorn
from api.v1 import films
from core import config
from core.logger import LOGGING
from db import kafka
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer


@lru_cache()
def get_settings():
    return config.Settings()

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka.kafka = AIOKafkaProducer(bootstrap_servers=f'{settings.kafka.host}:{settings.kafka.port}')
    await kafka.kafka.start()
    yield
    await kafka.kafka.stop()


app = FastAPI(
    title=settings.project_name,
    description="UGC - Сервис для хранения событий в Kafka",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(films.router, prefix='/api/v1/films', tags=['films'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
