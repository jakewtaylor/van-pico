#!/bin/sh

if [ -z "$1" ]; then
    echo "Usage: $0 <device>"
    exit 1
fi

echo "Uploading display code to" $1

# Clear the existing files on the device
mpremote connect $1 \
    + fs rm -rf lib \
    + fs rm -rf main.py \
    + fs mkdir lib \

# Copy the necessary files to the device
mpremote connect $1 \
    + fs cp -r src/modules :lib/modules \
    + fs cp src/main_display.py :main.py