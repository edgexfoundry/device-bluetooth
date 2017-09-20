#!/bin/sh

cd /edgex/edgex-resource-pygatt
source virtualenv/bin/activate
python $4 -p $5 &
cd /edgex/edgex-device-bluetooth

# Mapping container environment variable ADD_DEFAULT_DEVICE_PROFILES
# to service application.add-default-device-profiles property
if [ -z ${ADD_DEFAULT_DEVICE_PROFILES+x} ]; then
  PROFILES="" 
else 
  PROFILES="-Dapplication.add-default-device-profiles=$ADD_DEFAULT_DEVICE_PROFILES"
  echo "Running with extra arguments: $PROFILES"
fi

java  $2 $3 $PROFILES -jar $1
