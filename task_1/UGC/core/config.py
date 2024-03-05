from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

logging_config.dictConfig(LOGGING)


class AuthSettings(BaseSettings):
    secret_key: str = ...
    jwt_algorithm: str = ...
    model_config: str = SettingsConfigDict(env_prefix='auth_')


class RedisSettings(BaseSettings):
    host: str = ...
    port: int = ...
    model_config = SettingsConfigDict(env_prefix='redis_')


class KafkaSettings(BaseSettings):
    host: str = ...
    port: int = ...
    topic: str = ...
    model_config = SettingsConfigDict(env_prefix='kafka_')


class APPSettings(BaseSettings):
    project_name: str = 'UGS API'
    kafka: KafkaSettings = KafkaSettings()
    redis: RedisSettings = RedisSettings()
    auth: AuthSettings = AuthSettings()


settings = APPSettings()
