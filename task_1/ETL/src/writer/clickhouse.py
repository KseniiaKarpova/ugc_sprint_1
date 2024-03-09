from clickhouse_driver import Client
from clickhouse_driver import errors as ch_errors
from core.config import ClickHouseSettings
from models.event import UserAction
from utils.backoff import backoff
from writer import AbstractWriter


class ClickHouseWriter(AbstractWriter):
    """Класс для подключения к ClickHouse"""

    def __init__(self, conf: ClickHouseSettings):
        self.__conf = conf
        self.__client = None
        self.__connect()

    @backoff(error=(ch_errors.NetworkError, EOFError), start_sleep_time=2)
    def __connect(self):
        self.__client = Client(host=self.__conf.host)

    def __write_event(self, messages: list[UserAction]):
        self.__client.execute(
            "INSERT INTO default.events (user_id, film_id, action, created_at) VALUES",
            [(m.user_id, m.film_id, m.action, m.created_at) for m in messages]
        )

    def write(self, messages: list[UserAction]):
        """
        Метод записи сообщений в ClickHouse

        :param messages: список сообщений
        """
        try:
            self.__write_event(messages)
        except (ch_errors.NetworkError, EOFError):
            self.__connect()
            self.__write_event(messages)
