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
 * @microservice:  device-bluetooth
 * @author: Tyler Cox, Dell
 * @version: 1.0.0
 *******************************************************************************/

package org.edgexfoundry.ble;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.locks.ReentrantLock;
import org.edgexfoundry.domain.ScanList;
import org.jboss.resteasy.client.jaxrs.ResteasyClient;
import org.jboss.resteasy.client.jaxrs.ResteasyClientBuilder;
import org.jboss.resteasy.client.jaxrs.ResteasyWebTarget;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class PyGattClientImpl implements PyGattClient{

  @Value("${ble.pygatt.server}")
  private String pyGattServerURL;
  
  @Value("${ble.pygatt.backend}")
  private String pyGattBackend;
  
  private List<String> disconnected = new ArrayList<String>();
  
  private ReentrantLock lock = new ReentrantLock();
  
  public String setBackend() {
    lock.lock();
    try {
      return setBackend(pyGattBackend);
    } finally {
      lock.unlock();
    }
  }
  
  @Override
  public String setBackend(String backend) {
    lock.lock();
    try {
      return getClient().setBackend(backend);
    } finally {
      lock.unlock();
    }
  }

  @Override
  public String readFromUUID(String address, String uuid) {
    lock.lock();
    try {
      if(disconnected.contains(address))
        return null;
      return getClient().readFromUUID(address, uuid);
    } catch (Exception e) {
      disconnect(address);
      return null;
    } finally {
      lock.unlock();
    }
  }

  @Override
  public ScanList scanForDevices(String timeout) {
    lock.lock();
    try {
      ScanList scanList = getClient().scanForDevices(timeout);
      for (Map<String, String> device: scanList.getScan())
        removeDisconnected(device.get("address"));
      return scanList;
    } finally {
      lock.unlock();
    }
  }

  @Override
  public String writeToUUID(String address, String uuid, String value) {
    lock.lock();
    try {
      if(disconnected.contains(address))
        return null;
      return getClient().writeToUUID(address, uuid, value);
    } catch (Exception e) {
      disconnect(address);
      return null;
    } finally {
      lock.unlock();
    }
    
  }
  
  private PyGattClient getClient() {
    ResteasyClient client = new ResteasyClientBuilder().build();
    ResteasyWebTarget target = client.target(pyGattServerURL);
    return target.proxy(PyGattClient.class);
  }

  @Override
  public String disconnect(String address) {
    lock.lock();
    try {
      if(disconnected.contains(address))
        return null;
      addDisconnected(address);
      return getClient().disconnect(address);
    } finally {
      lock.unlock();
    }
  }

  @Override
  public String initialize() {
    lock.lock();
    try {
      return getClient().initialize();
    } finally {
      lock.unlock();
    }
  }
  
  private void addDisconnected(String address) {
    disconnected.add(address);
  }

  private void removeDisconnected(String address) {
    disconnected.remove(address);
  }
}
