from airflow.decorators import dag, task
from airflow_provider_kafka.operators.consume_from_topic import ConsumeFromTopicOperator
from clickhouse_driver import Client
import json
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# only change the topic name if you are using your own Kafka cluster/topic
KAFKA_TOPIC = "event"
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DATABASE = "analytics"
CLICKHOUSE_TABLE = "events"


def save_data_to_clickhouse(data):
    "Takes in consumed messages and saves them to ClickHouse."
    client = Client(host='localhost')
    logger.info(client.execute('SHOW DATABASES'))
    logger.info(client.execute('CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER company_cluster'))
    #client.execute('CREATE TABLE analytics.events ON CLUSTER company_cluster (id Int64, x Int32) Engine=MergeTree() ORDER BY id')

    key = json.loads(data.key())
    message_content = json.loads(data.value())
    logger.info(message_content)

    # Adjust the following line based on your ClickHouse table structure
    query = f"INSERT INTO {CLICKHOUSE_TABLE} VALUES (%s, %s)"  # Example query

    client.execute(query, (key, json.dumps(message_content)))

    client.disconnect()

KAFKA_HOST='kafka-0'
KAFKA_PORT=9092
KAFKA_TOPIC='event'

@dag(
    start_date=datetime(2023, 3, 8),
    schedule_interval=None,  # Set to None for manual triggering or define your schedule
    catchup=False,
    render_template_as_native_obj=True
)
def consume_treats():
    consume_treats = ConsumeFromTopicOperator(
        task_id="consume_treats",
        topics=[KAFKA_TOPIC],
        consumer_config={
            "bootstrap.servers": "kafka-0:9092",
            "enable.auto.commit": False,
            "auto.offset.reset": "beginning",
        },
        commit_cadence="end_of_batch",
        apply_function=save_data_to_clickhouse,
        poll_timeout=20,
        max_messages=1000,
    )

    consume_treats


consume_treats()