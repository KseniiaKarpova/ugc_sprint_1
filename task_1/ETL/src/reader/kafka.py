import json

from core.config import KafkaSettings
from kafka import KafkaConsumer
from kafka import errors as kafka_errors
from models.event import UserAction
from reader import AbstractReader
from utils.backoff import backoff


class KafkaReader(AbstractReader):
    """Класс для подключения к Kafka"""
    def __init__(self, conf: KafkaSettings):
        self.__conf = conf
        self.__consumer = None
        self.__connect()

    @backoff(error=kafka_errors.NoBrokersAvailable)
    def __connect(self):
        self.__consumer = KafkaConsumer(
            self.__conf.topic,
            bootstrap_servers=[self.__conf.host],
            auto_offset_reset=self.__conf.auto_offset_reset,
            enable_auto_commit=self.__conf.enable_auto_commit,
            group_id=self.__conf.group_id,
        )

    def read_data(self) -> list[UserAction]:
        """
        Метод для чтения сообщений из Kafka
        """
        for message in self.__consumer:
            message = json.loads(message.value.decode('utf8'))

            yield UserAction(
                action=message['action'],
                user_id=message['user_id'],
                film_id=message['film_id'],
                created_at=message['created_at'],
            )

    def commit(self):
        """Метод для подтверждения прочтения сообщения."""

        self.__consumer.commit()
