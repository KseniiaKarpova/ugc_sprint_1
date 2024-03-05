#!/bin/sh

echo "Waiting for kafka-0"
while ! (nc -z kafka-0 9092 ); do
  sleep 0.1
done
exec "$@"