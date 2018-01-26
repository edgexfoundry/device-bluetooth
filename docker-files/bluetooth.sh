#!/bin/sh
# Copyright 2016-2017 Dell Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @microservice:  device-bacnet
# @author: Tyler Cox, Dell
# @version: 1.0.0
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
