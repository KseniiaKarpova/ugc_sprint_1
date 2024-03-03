from logging import config as logging_config

from core.logger import LOGGING
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

logging_config.dictConfig(LOGGING)


class KafkaSettings(BaseSettings):
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(env_prefix='kafka_')


class APPSettings(BaseSettings):
    project_name: str = 'UGS API'
    kafka: KafkaSettings = KafkaSettings()


settings = APPSettings()
