#!/bin/sh

set -e

. .venv/bin/activate

service cron start

exec python tg_bot.py