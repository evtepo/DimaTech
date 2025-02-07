#!/usr/bin/env bash

attempts=5

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT && [ $attempts -gt 0 ]; do
    echo "Waiting for PostgreSQL. Attempts left: $attempts"
    sleep 1
    attempts=$((attempts - 1))
done

if nc -z $POSTGRES_HOST $POSTGRES_PORT; then
    echo "PostgreSQL is up!"
    alembic upgrade head
    gunicorn main:app --bind 0.0.0.0:8000 --workers 3 -k uvicorn.workers.UvicornWorker
else
    echo "Failed to connect to PostgreSQL after 5 attempts. Exiting."
    exit 1
fi