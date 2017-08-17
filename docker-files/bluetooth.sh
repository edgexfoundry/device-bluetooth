#!/bin/sh

ls /
cd /edgex/edgex-resource-pygatt
source virtualenv/bin/activate
python $4 -p $5 &
cd /edgex/edgex-device-bluetooth
java  $2 $3 -jar $1