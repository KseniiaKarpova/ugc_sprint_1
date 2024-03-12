#!/bin/sh

echo "Waiting for kafka-0"
while ! (nc -z $KAFKA_HOST $KAFKA_PORT ); do
  sleep 0.1
done
exec "$@"