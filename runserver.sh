#!/bin/sh
set -eu

exec uvicorn unicorn:app --host 0.0.0.0 --port "${PORT:-5000}"
