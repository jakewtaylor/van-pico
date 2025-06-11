#!/bin/sh

if [ -z "$1" ]; then
    echo "Usage: $0 <device>"
    exit 1
fi

echo "Uploading can test to" $1

mpremote connect $1 \
    + fs cp -r src/modules :modules \
    + fs cp src/main_can_sender_test.py :main.py