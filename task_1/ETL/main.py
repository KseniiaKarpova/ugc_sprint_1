from airflow.decorators import dag, task
from pendulum import datetime
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
import json
from clickhouse_driver import Client

# only change the topic name if you are using your own Kafka cluster/topic
KAFKA_TOPIC = "event"
CLICKHOUSE_HOST = "your_clickhouse_host"
CLICKHOUSE_PORT = 9000
CLICKHOUSE_DATABASE = "your_database"
CLICKHOUSE_TABLE = "your_table"


def save_data_to_clickhouse(data):
    "Takes in consumed messages and saves them to ClickHouse."
    client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT, database=CLICKHOUSE_DATABASE)
    key = json.loads(data.key())
    message_content = json.loads(data.value())
    
    # Adjust the following line based on your ClickHouse table structure
    query = f"INSERT INTO {CLICKHOUSE_TABLE} VALUES (%s, %s)"  # Example query
    
    client.execute(query, (key, json.dumps(message_content)))

    client.disconnect()


@dag(
    start_date=datetime(2023, 4, 1),
    schedule_interval=None,  # Set to None for manual triggering or define your schedule
    catchup=False,
    render_template_as_native_obj=True,
)
def consume_treats():
    consume_treats = ConsumeFromTopicOperator(
        task_id="consume_treats",
        kafka_config_id="kafka_default",
        topics=[KAFKA_TOPIC],
        apply_function=save_data_to_clickhouse,
        poll_timeout=20,
        max_messages=1000,
    )

    consume_treats


consume_treats()
