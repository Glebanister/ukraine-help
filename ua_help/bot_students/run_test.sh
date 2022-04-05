#!/usr/bin/env bash

mkdir -p /app/clients_data/v1/test
bash -c 'python main.py --root /app/ua_help/bot_students/ --config /app/ua_help/bot_students/resources/config_test.json'
