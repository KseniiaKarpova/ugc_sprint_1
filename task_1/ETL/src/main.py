import gc
import time

from core.config import ClickHouseSettings, KafkaSettings
from core.logger import logger
from reader.kafka import KafkaReader
from writer.clickhouse import ClickHouseWriter

kafka_settings = KafkaSettings()
clickhouse_settings = ClickHouseSettings()


def main():
    kafka = KafkaReader(kafka_settings)
    clickhouse = ClickHouseWriter(clickhouse_settings)
    messages = []
    start = time.time()
    for message in kafka.read_data():
        messages.append(message)
        if time.time() - start > clickhouse_settings.wait_time:
            clickhouse.write(messages)
            kafka.commit()
            logger.debug(f'Add {len(messages)} rows')
            messages = []
            gc.collect()
            start = time.time()


if __name__ == '__main__':
    main()
