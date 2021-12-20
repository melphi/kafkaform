#!/bin/bash

set -e

source .venv/bin/activate
python3 -m mypy app/app.py
python3 -m unittest
