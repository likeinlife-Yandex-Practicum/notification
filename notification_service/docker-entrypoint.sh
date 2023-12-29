#!/bin/sh

if [ "$1" = "notify" ]; then
  python src/notification_worker.py
elif [ "$1" = "user" ]; then
  python src/user_provider_worker.py
else
  echo "Unknown command argument: $1"
fi