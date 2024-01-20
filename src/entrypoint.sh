#!/bin/sh

echo "Waiting for mongo..."

while ! nc -z dealer-imitator-mongodb-srv 27017; do
  sleep 0.1
done

echo "Mongo started"


exec "$@"
