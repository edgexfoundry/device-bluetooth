from Expiring import Expiring
import pygatt.backends
import atexit
from BGAPIBackend import BGBackend
from GATTBackend import GATTBackend

from pygatt.exceptions import NotConnectedError, BLEError, NotificationTimeout
from pygatt.backends.bgapi.exceptions import ExpectedResponseTimeout, BGAPIError
from serial import SerialException
import time    

gatt = GATTBackend
bgapi = BGBackend

class ConnectionTools(object):

    def __init__(self, new_backend = "gatt", cache_size=20, max_age=180):
        self.backend = None
        self.adapter = None
        self.max_age = max_age
        self.characteristics = {}
        self.cache_size = cache_size
        self.connection_cache = None
        self.set_backend(new_backend)
        self.new_cache()
        atexit.register(self.cleanup)

    def new_cache(self):
        self.connection_cache = Expiring(max_len=self.cache_size, max_age_seconds=self.max_age)
        self.connection_cache.manager()

    def get_backend(self):
        if self.backend == gatt:
            return "gatt"
        if self.backend == bgapi:
            return "bgapi"
        return ""

    def set_backend(self,new_backend):
        initial = self.backend
        if new_backend == "gatt":
            self.backend = gatt
        if new_backend == "bgapi":
            self.backend = bgapi
        if initial != self.backend:
            self.new_cache()
            try:
                self.new_connection()
            except (OSError, BGAPIError):
                print "Adapter not found, trying alternative"
                time.sleep(1)
                if new_backend == "gatt":
                    return self.set_backend("bgapi")
                if new_backend == "bgapi":
                    return self.set_backend("gatt")
        return new_backend

    def new_connection(self):
        if self.adapter is not None:
            try:
                self.adapter.stop()
            except (AttributeError):
                pass
        self.adapter = self.backend()
        self.adapter.start()

    def connect(self,address,retry=False):
        con = None
        try:
            if self.adapter is None:
                 self.new_connection()
            if address not in self.connection_cache:
                con = self.adapter.connect(address)
                self.connection_cache[address] = con
            else:
                con = self.connection_cache[address]
                self.connection_cache[address] = con
        except NotConnectedError, ExpectedResponseTimeout:
            self.disconnect(address)
            self.new_connection()
            if not retry:
                return self.connect(address, True)
            raise NotConnectedError()
        if address in self.characteristics:
            con._characteristics = self.characteristics[address]
        return con

    def disconnect(self,address):
        if address in self.connection_cache:
            con = self.connection_cache[address]
            del self.connection_cache[address]
            con.disconnect()

    def scan(self,scan_time,retry=False):
        scanVals = ""
        if self.adapter is None:
            self.new_connection()
        try:
            scanVals = self.adapter.scan(scan_time)
        except NotConnectedError, SerialException:
            print "not connected"
            self.set_backend(self.get_backend())
            if not retry:
                return self.scan(scan_time,True)
        return scanVals

    def cleanup(self):
        print "exiting"
        for key in self.connection_cache:
            print key
            connect = self.connection_cache[key]
            connect.disconnect()
        if self.adapter is not None:
            self.adapter.stop()
