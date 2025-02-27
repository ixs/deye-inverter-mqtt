# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from deye_command_handlers import DeyeActivePowerRegulationCommandHandler
from deye_modbus import DeyeModbus
from deye_mqtt import DeyeMqttClient
from deye_config import DeyeConfig, DeyeMqttConfig
from paho.mqtt.client import Client, MQTTMessage


class TestDeyeActivePowerRegulationCommandHandler:
    @staticmethod
    @pytest.fixture
    def modbus_mock(mocker) -> DeyeModbus:
        return mocker.Mock(spec=DeyeModbus)

    @staticmethod
    @pytest.fixture
    def mqtt_client_mock(mocker) -> DeyeMqttClient:
        return mocker.Mock(spec=DeyeMqttClient)

    @staticmethod
    @pytest.fixture
    def mqtt_config_mock(mocker) -> DeyeMqttConfig:
        return mocker.Mock(spec=DeyeMqttConfig)

    @staticmethod
    @pytest.fixture
    def config_mock(mocker, mqtt_config_mock) -> DeyeConfig:
        mock = mocker.Mock(spec=DeyeConfig)
        mock.mqtt = mqtt_config_mock
        return mock

    def test_handle_valid_value(self, modbus_mock: DeyeModbus):
        # given
        sut = DeyeActivePowerRegulationCommandHandler(modbus_mock)

        # and
        msg = MQTTMessage()
        msg.payload = "100"

        # when
        sut.handle_command(None, None, msg)

        # then
        modbus_mock.write_register.assert_called_with(40, 1000)

    def test_reject_too_high_value(self, modbus_mock: DeyeModbus):
        # given
        sut = DeyeActivePowerRegulationCommandHandler(modbus_mock)

        # and
        msg = MQTTMessage()
        msg.payload = "121"

        # expect
        sut.handle_command(None, None, msg)

        # then
        assert not modbus_mock.write_register.called

    def test_reject_too_low_value(self, modbus_mock: DeyeModbus):
        # given
        sut = DeyeActivePowerRegulationCommandHandler(modbus_mock)

        # and
        msg = MQTTMessage()
        msg.payload = "-1"

        # expect
        sut.handle_command(None, None, msg)

        # then
        assert not modbus_mock.write_register.called
