import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import action
from core.config import settings
from core.logger import LOGGING
from db import kafka, redis
from fastapi import FastAPI, status, Request
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from utils.jaeger import configure_tracer, tracer
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from utils.constraint import RequestLimit
from opentelemetry.trace import SpanKind



@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.jaeger.enable:
        configure_tracer(
            host=settings.jaeger.host,
            port=settings.jaeger.port,
            service_name=settings.project_name)
    kafka.kafka = AIOKafkaProducer(
        loop=asyncio.get_event_loop(),
        bootstrap_servers=f'{settings.kafka.host}:{settings.kafka.port}')
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

@app.middleware('http')
async def before_request(request: Request, call_next):
    user = request.headers.get('X-Forwarded-For')
    result = await RequestLimit().is_over_limit(user=user)
    if result:
       return ORJSONResponse(
           status_code=status.HTTP_429_TOO_MANY_REQUESTS,
           content={'detail': 'Too many requests'}
       )

    response = await call_next(request)
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={
                'detail': 'X-Request-Id is required'})
    path = request.url.path
    method = request.method
    with tracer.start_as_current_span(f"HTTP {method} {path}", kind=SpanKind.SERVER) as span:
        span.set_attribute("http.method", method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.request_id", request_id)
        response = await call_next(request)
        span.set_attribute("http.status_code", response.status_code)
        return response

FastAPIInstrumentor.instrument_app(app)

app.include_router(action.router, prefix='/api/v1/action', tags=['films'])


if __name__ == '__main__':
    uvicorn.run(
        app,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
