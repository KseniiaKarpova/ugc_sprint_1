from typing import Optional

from redis.asyncio import Redis

redis: Redis | None = None


def get_redis() -> Redis | None:
    return redis
