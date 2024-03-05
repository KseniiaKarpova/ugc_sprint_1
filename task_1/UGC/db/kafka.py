from aiokafka import AIOKafkaProducer


kafka: None | AIOKafkaProducer = None


def get_kafka() -> AIOKafkaProducer:
    return kafka
