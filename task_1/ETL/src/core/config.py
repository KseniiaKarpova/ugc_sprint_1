from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class KafkaSettings(BaseSettings):
    host: str = ...
    port: int = ...
    topic: str = ...
    auto_offset_reset: str = 'earliest'
    enable_auto_commit: bool = False
    group_id: str = 'analytics'
    model_config = SettingsConfigDict(env_prefix='kafka_')


class ClickHouseSettings(BaseSettings):
    host: str = ...
    port: int = ...
    wait_time: int = 1

    model_config = SettingsConfigDict(env_prefix='clickhouse_')


class LoggerSettings(BaseSettings):
    """Конфиг логирования."""

    version: int = 1
    disable_existing_loggers: bool = False

    formatters: dict = {
        "default_formatter": {
            "format": '%(levelname)s\t%(asctime)s\t%(funcName)s\t"%(message)s"'
        },
    }

    handlers: dict = {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": "logs.log",
            "formatter": "default_formatter",
        },
        "stream_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
        },
    }

    loggers: dict = {
        "etl_logger": {
            "handlers": ["stream_handler"],
            "level": "DEBUG",
            "propagate": True,
        }
    }
