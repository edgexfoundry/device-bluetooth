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
