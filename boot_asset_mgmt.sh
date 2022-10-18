#!/bin/bash

while ! nc -z $NATS_HOST $NATS_PORT; do
  sleep 0.5;
done;
echo "Connected to NATS";

exec python -u pfx-asset_mgmt.py
