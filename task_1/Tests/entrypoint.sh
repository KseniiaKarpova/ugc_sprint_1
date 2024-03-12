#!/bin/sh

echo "Waiting for test-kafka-0"
while ! (nc -z $KAFKA_HOST $KAFKA_PORT && nc -z $AUTH_POSTGRES_HOST $AUTH_POSTGRES_PORT  ); do
  sleep 0.1
done
pytest functional/src/
exec "$@"