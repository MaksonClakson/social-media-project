#!/bin/sh
celery -A core.celery worker --loglevel=info
