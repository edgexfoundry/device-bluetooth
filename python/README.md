Main Author: Tyler Cox

Language: Python

Copyright 2016-2017, Dell, Inc.

PyGatt Resource Library interface for BLE Device Serivce - A device service that uses Bluetooth LowEnergy to communicate with devices that support get/set operations.  
Establishes a framework for interacting with BLE devices through defineable commands. Supports BGAPI with a Silicon Labs specific dongle and Pygatt directly. If BLE device 
is communicating over Pygatt interface in Linux, it requires BlueZ 5.35 and above to be installed.

### Modification ###

Once modified, please update the tar package for deployment using

```
#!shell

python setup.py sdist
```


### Setup/Initialization ###

 
* python-setuptools
* python-dev
* pygatt==0.13.1
* flask-restful==0.3.4
* pyyaml==3.11
* requests==2.4.3

### Configuring ###


or create a virtual env to test out a package


```
#!shell

   virtualenv pygattresource
   . pygattresource/bin/activate
   pip install <path to tar.gz file>
   FlaskController.py -p 5000
```


