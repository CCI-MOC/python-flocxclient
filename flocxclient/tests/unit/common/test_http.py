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

import mock
import pytest
import testtools


from flocxclient.common import http
from flocxclient.tests.unit import utils


DEFAULT_TIMEOUT = 600

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '1234'


def _session_client(**kwargs):
    return http.SessionClient(os_flocx_api_version='1.6',
                              interface='publicURL',
                              service_type='market',
                              region_name='',
                              auth=None,
                              **kwargs)


class SessionClientTest(testtools.TestCase):

    def test_json_request(self):
        session = utils.mockSession({})

        client = _session_client(session=session)
        resp, body = client.json_request('GET', 'url')

        session.request.assert_called_once_with(
            'url', 'GET',
            raise_exc=False,
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json',
                     'X-OpenStack-Flocx-API-Version': '1.6'},
            user_agent=http.USER_AGENT,
            auth=None,
            endpoint_filter={
                'interface': 'publicURL',
                'service_type': 'market',
                'region_name': ''
            },
        )

        self.assertEqual(resp, session.request.return_value)
        self.assertEqual(body, [])

    @mock.patch.object(http.SessionClient, 'get_endpoint', autospec=True)
    def test_endpoint_not_found(self, mock_get_endpoint):
        mock_get_endpoint.return_value = None

        with pytest.raises(Exception):
            _session_client(session=utils.mockSession({}))
