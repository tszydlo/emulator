#!/bin/sh
export MRAA_FOGDEVICES_PLATFORM_ID="$1"
export MRAA_FOGDEVICES_PLATFORM_BROKER="iot.eclipse.org"
python /root/artik_lm35.py $2 $3
