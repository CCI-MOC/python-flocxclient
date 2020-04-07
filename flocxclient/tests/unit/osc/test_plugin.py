#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import unittest.mock as mock
import testtools

from flocxclient.osc import plugin
from flocxclient.tests.unit.osc import fakes
from flocxclient.v1 import client


class MakeClientTest(testtools.TestCase):

    @mock.patch.object(client, 'Client')
    def test_make_client_explicit_version(self, mock_client):
        instance = fakes.FakeClientManager()
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_flocx_api_version=fakes.API_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)

    @mock.patch.object(client, 'Client')
    def test_make_client_latest(self, mock_client):
        instance = fakes.FakeClientManager()
        instance._api_version = {'market': plugin.LATEST_VERSION}
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_flocx_api_version=plugin.LATEST_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)

    @mock.patch.object(client, 'Client')
    def test_make_client_v1(self, mock_client):
        instance = fakes.FakeClientManager()
        instance._api_version = {'market': '1.0'}
        plugin.make_client(instance)
        mock_client.assert_called_once_with(
            os_flocx_api_version=plugin.LATEST_VERSION,
            session=instance.session,
            region_name=instance._region_name,
            endpoint_override=None)
