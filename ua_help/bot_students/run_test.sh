#!/usr/bin/env bash

mkdir -p /root/clients_data/v1/release
bash -c 'python main.py --root /root/ukraine-help/ua_help/bot_students/ --config /root/ukraine-help/ua_help/bot_students/resources/config_test.json'
