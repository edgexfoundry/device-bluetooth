/*******************************************************************************
 * Copyright 2016-2017 Dell Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @microservice: device-bluetooth
 * @author: Tyler Cox, Dell
 * @version: 1.0.0
 *******************************************************************************/

package org.edgexfoundry.ble;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import javax.ws.rs.InternalServerErrorException;
import javax.ws.rs.ProcessingException;
import org.edgexfoundry.ble.PyGattClient;
import org.edgexfoundry.data.DeviceStore;
import org.edgexfoundry.data.ObjectStore;
import org.edgexfoundry.data.ProfileStore;
import org.edgexfoundry.domain.BleAttribute;
import org.edgexfoundry.domain.BleObject;
import org.edgexfoundry.domain.ScanList;
import org.edgexfoundry.domain.meta.Addressable;
import org.edgexfoundry.domain.meta.Device;
import org.edgexfoundry.domain.meta.ResourceOperation;
import org.edgexfoundry.exception.controller.ServiceException;
import org.edgexfoundry.handler.BleHandler;
import org.edgexfoundry.support.logging.client.EdgeXLogger;
import org.edgexfoundry.support.logging.client.EdgeXLoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class BleDriver {

  private static final EdgeXLogger logger =
      EdgeXLoggerFactory.getEdgeXLogger(BleDriver.class);

  @Autowired
  ProfileStore profiles;

  @Autowired
  DeviceStore devices;

  @Autowired
  ObjectStore objectCache;

  @Autowired
  BleHandler handler;

  @Autowired
  PyGattClient pyGattClient;

  @Value("${ble.pygatt.backend}")
  private String bleBackend;

  @Value("${ble.pygatt.server}")
  private String bleServer;

  @Value("${ble.scan.time:0.25}")
  private String m_scantime;

  private Boolean initialized = false;

  public ScanList discover() {
    ScanList availableList = null;
    if (initialized == false) {
      if (!initialize()) throw new ServiceException(new Exception("Cannot initialize interface"));
    }
    // Fill with BLE specific discovery mechanism
    try {
      availableList = pyGattClient.scanForDevices(m_scantime);
      logger.info(availableList.toString());
    } catch (InternalServerErrorException e) {
      availableList = null;
    } catch (ProcessingException e) {
      availableList = null;
    }
    return availableList;
  }

  // operation is get or set
  // Device to be written to
  // BLE Object to be written to
  // value is string to be written or null
  public void process(ResourceOperation operation, Device device, BleObject object,
      String value, String transactionId, String opId) {
    String result = "";
    if (initialized == false) {
      if (!initialize()) throw new ServiceException(new Exception("Cannot initialize interface"));
    }
    result = processCommand(operation.getOperation(), device.getAddressable(), object.getAttributes(), value);
    if (result == null)
      devices.remove(device.getId());
    objectCache.put(device, operation, result);
    handler.completeTransaction(transactionId, opId, objectCache.getResponses(device, operation));
  }

  public String processCommand(String operation, Addressable addressable,
      BleAttribute attributes, String value) {
    String address = addressable.getPath();
    String uuid = attributes.getUuid();
    String result = ""; 
    logger.info("ProcessCommand: " + operation + ", addressable: "
      + addressable + ", attributes: " + attributes + ", value: " + value );
    try{
      if(operation.equals("get")){
        result = pyGattClient.readFromUUID(address, uuid);
      } else if(operation.equals("set")){
        result = pyGattClient.writeToUUID(address, uuid, value);
      }
      JsonObject args = new JsonParser().parse(result).getAsJsonObject();
      if (result.contains("value"))
        result = args.get("value").getAsString();
      if (result.equals("error"))
        throw new Exception();
    } catch(Exception e) {
      result = null;
      logger.error("Device is not connected. Switch on the device "
        + "and allow the device service to pair automatically.");
      logger.error("Address: " + address + " UUID: " + uuid + " Value: " + value);
    }
    return result;
  }

  public boolean initialize() {
    try {
      pyGattClient.setBackend(bleBackend);
      initialized = true;
    } catch (Exception e) {
      logger.error("PyGatt Controller service at: " + bleServer + " is not reachable.");
      return false;
    }
    pyGattClient.initialize();
    return true;
  }

  public void disconnectDevice(Addressable address) {
    pyGattClient.disconnect(address.getPath());
  }
}
