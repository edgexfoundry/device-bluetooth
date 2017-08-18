import binascii
import json
import collections
import struct
import array

from ConnectionTools import ConnectionTools
from pygatt.exceptions import NotConnectedError
from pygatt.backends.bgapi.exceptions import ExpectedResponseTimeout

pgc = ConnectionTools()

def get_backend(new_backend):
    return pgc.get_backend()

def set_backend(new_backend):    
    return pgc.set_backend(new_backend)

def char_read(address, uuid, retry = False):
    bytes = "error"
    try:
        con = pgc.connect(address)
        bytes = con.char_read(uuid)
    except NotConnectedError, ExpectedResponseTimeout:
        disconnect(address)
        if (retry == False):
            return char_read(address,uuid,True)
    return bytes

def char_write(address, index, value, retry = False):
    try:
        con = pgc.connect(address)
        handle = None
        if len(index) > 32:
            if con._characteristics == {}:
                characteristics(address)
            handle = con.get_handle(index)
            pgc.connection_cache[address] = con
        else:
            handle = index
        value_array = bytearray.fromhex(value)    
        con.char_write_handle(handle,value_array,False)
    except NotConnectedError, ExpectedResponseTimeout:
        disconnect(address)
        if (retry == False):
            return char_write(address,index,value,True)
    return value_array

def characteristics(address, retry = False):
    try:
        con = pgc.connect(address)
        if con._characteristics == {}:
            characters = con.discover_characteristics()
            con._characteristics = characters
            pgc.characteristics[address] = characters
            pgc.connection_cache[address] = con
        else:
            characters = con._characteristics
    except NotConnectedError, ExpectedResponseTimeout:
        disconnect(address)
        if (retry == False):
            return characteristics(address, True)
    return characters

def scan(scan_time = 2.0, retry = False):
    scanVals = pgc.scan(scan_time)
    return scanVals

def active_connections():
    return pgc.connection_cache.keys()
    
def active_characteristics():
    return pgc.characteristics    

def disconnect(address, retry = False):
    try:
        con = pgc.disconnect(address)
    except NotConnectedError, ExpectedResponseTimeout:
        if (retry == False):
            return disconnect(address,True)
    return None
