#!/usr/bin/env bash

set -e

export KAFKA_BROKER_ADDRESS=localhost:9092
export KAFKA_CONNECT_URL=http://localhost:8083
export KAFKA_KSQL_URL=http://localhost:8088

source .venv/bin/activate
python3 -m app.app $@
