#!/bin/sh

# Инициализация БД в RAM
if [ ! -f "/app/ram_db/db.sqlite3" ]; then
    python manage.py migrate --noinput
fi

exec "$@"