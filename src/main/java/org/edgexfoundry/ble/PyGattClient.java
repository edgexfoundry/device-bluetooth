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

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import org.edgexfoundry.domain.ScanList;

public interface PyGattClient {
  
  @GET
  @Path("/initialize")
  String initialize();

  @GET
  @Path("/scan/{timeout}")
  ScanList scanForDevices(@PathParam("timeout") String timeout);
  
  @GET
  @Path("/{address}/read/{uuid}")
  String readFromUUID(@PathParam("address") String address, @PathParam("uuid") String uuid);

  @GET
  @Path("/{address}/write/{uuid}/{value}")
  String writeToUUID(@PathParam("address") String address, @PathParam("uuid") String uuid,
    @PathParam("value") String value);
  
  @GET
  @Path("/backend/{backend}")
  String setBackend(@PathParam("backend") String backend);
  
  @GET
  @Path("/{address}/disconnect")
  String disconnect(@PathParam("address") String address);
}
