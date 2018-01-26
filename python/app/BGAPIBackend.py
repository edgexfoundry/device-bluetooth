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
import pygatt.backends
from pygatt.backends.bgapi.bgapi import *


class BGBackend(pygatt.backends.BGAPIBackend):
    def __init__(self):
        pygatt.backends.BGAPIBackend.__init__(self)
        
    def discover_characteristics(self, connection_handle):
        att_handle_start = 0x0001  # first valid handle
        att_handle_end = 0xFFFF  # last valid handle
        log.info("Fetching characteristics for connection %d",
             connection_handle)
        self.send_command(
            CommandBuilder.attclient_find_information(
                connection_handle, att_handle_start, att_handle_end))

        self.expect(ResponsePacketType.attclient_find_information)
        self.expect(EventPacketType.attclient_procedure_completed,
                    timeout=20)

        for char_uuid_str, char_obj in (
                self._characteristics[connection_handle].iteritems()):
            log.info("Characteristic 0x%s is handle 0x%x",
                     char_uuid_str, char_obj.handle)
            for desc_uuid_str, desc_handle in (
                    char_obj.descriptors.iteritems()):
                log.info("Characteristic descriptor 0x%s is handle 0x%x",
                         desc_uuid_str, desc_handle)
        return self._characteristics[connection_handle]

    @staticmethod
    def _get_uuid_type(uuid):
        """
        Checks if the UUID is a custom 128-bit UUID or a GATT characteristic
        descriptor UUID.

        uuid -- the UUID as a bytearray.

        Return a UUIDType.
        """
        if len(uuid) == 16:  # 128-bit --> 16 byte
            return UUIDType.custom
        if uuid in constants.gatt_service_uuid.values():
            return UUIDType.service
        if uuid in constants.gatt_attribute_type_uuid.values():
            return UUIDType.attribute
        if uuid in constants.gatt_characteristic_descriptor_uuid.values():
            return UUIDType.descriptor
        if uuid in constants.gatt_characteristic_type_uuid.values():
            return UUIDType.characteristic
        log.info("UUID %s is of unknown type")
        return UUIDType.custom
        
    def _ble_evt_attclient_find_information_found(self, args):
        """
        Handles the event for characteritic discovery.

        Adds the characteristic to the dictionary of characteristics or adds
        the descriptor to the dictionary of descriptors in the current
        characteristic. These events will be occur in an order similar to the
        following:
        1) primary service uuid
        2) 0 or more descriptors
        3) characteristic uuid
        4) 0 or more descriptors
        5) repeat steps 3-4

        args -- dictionary containing the characteristic handle ('chrhandle'),
        and characteristic UUID ('uuid')
        """
        raw_uuid = bytearray(reversed(args['uuid']))
        uuid_type = self._get_uuid_type(raw_uuid)
        if uuid_type != UUIDType.custom or len(raw_uuid) != 16:
            uuid = uuid16_to_uuid(int(
                bgapi_address_to_hex(args['uuid']).replace(':', ''), 16))
        else:
            uuid = UUID(hexlify(raw_uuid))

        # TODO is there a way to get the characteristic from the packet instead
        # of having to track the "current" characteristic?
        if (uuid_type == UUIDType.descriptor and
                self._current_characteristic is not None):
            self._current_characteristic.add_descriptor(uuid, args['chrhandle'])
        elif uuid_type == UUIDType.custom:
            log.info("Found custom characteristic %s" % uuid)
            new_char = Characteristic(uuid, args['chrhandle'])
            self._current_characteristic = new_char
            self._characteristics[
                args['connection_handle']][uuid] = new_char    