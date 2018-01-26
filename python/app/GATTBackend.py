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
from __future__ import print_function
import subprocess
import sys
import logging
import pygatt.backends
from pygatt.backends.gatttool import *
from pygatt.backends.gatttool.gatttool import *
dir(pygatt.backends.gatttool.gatttool)
try:
    import pexpect
except Exception as err:
    if platform.system() != 'Windows':
        print("WARNING:", err, file=sys.stderr)

log = logging.getLogger(__name__)

class GATTBackend(pygatt.backends.GATTToolBackend):
    def __init__(self, hci_device='hci0', gatttool_logfile=None,
                 cli_options=None):
        pygatt.backends.GATTToolBackend.__init__(self, hci_device='hci0', gatttool_logfile=None,
                 cli_options=None)

    def reset(self):
        result = subprocess.Popen(["sudo", "systemctl", "restart", "bluetooth"]).wait()
        if result != 0:
            subprocess.Popen(["sudo", "service", "bluetooth", "restart"]).wait()
        subprocess.Popen([
            "sudo", "hciconfig", self._hci_device, "reset"]).wait()
