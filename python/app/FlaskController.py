#!/usr/bin/env python
from flask import Flask
from flask.json import jsonify
from uuid import UUID
import collections
import binascii

from ClientController import *

app = Flask(__name__)

def convert(data):
    if isinstance(data, bytearray):
        return "0x" + binascii.hexlify(data)
    elif isinstance(data, (UUID,basestring)):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    elif "__dict__" in dir(data):
        return dict(map(convert, data.__dict__.iteritems()))
    else:
        return data

@app.route("/api/v1/ping")
def flask_ping():
    return "pong"
        
@app.route("/backend")
def flask_get_backend():
    return get_backend()

@app.route("/backend/<string:new_backend>")
def flask_set_backend(new_backend):
    backend = set_backend(new_backend)
    return backend

@app.route("/<address>/disconnect")    
def flask_disconnect(address):
    disconnect(address)
    return "{}"

@app.route("/device")
def flask_active_connections():
    connections = active_connections()
    return jsonify(connections=connections)
    
@app.route("/characteristics")
def flask_active_characteristics():
    all_characteristics = active_characteristics()
    return jsonify(characteristics=all_characteristics)   
    
@app.route("/initialize")
def flask_initialize():
    connections = active_connections()
    for address in connections:
        disconnect(address)
    return "{}"    

@app.route("/<address>/read/<uuid>")
def flask_char_read(address, uuid):
    bytes = convert(char_read(address,uuid))
    return jsonify(value=bytes)

@app.route("/<address>/write/<index>/<value>")
def flask_char_write(address, index, value):
    bytes = convert(char_write(address,index,value))
    return jsonify(value=bytes)

@app.route("/<address>/characteristics")
def flask_characteristics(address):
    characters = convert(characteristics(address))
    return jsonify(characteristics=characters)

@app.route("/scan/<scan_time>")
def flask_scan(scan_time = 2.0):
    scan_time = float(scan_time)
    scan_val = convert(scan(scan_time))
    return  jsonify(scan=scan_val)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,threaded=True)

