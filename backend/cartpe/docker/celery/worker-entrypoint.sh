#!/bin/sh

# run a celery worker :)
celery -A cartpe worker --loglevel=info --concurrency 1 -E