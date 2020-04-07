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

import logging

from keystoneauth1 import adapter
from oslo_serialization import jsonutils
from http import client as http_client

DEFAULT_VER = '1.0'
LAST_KNOWN_API_VERSION = 1
LATEST_VERSION = '1.{}'.format(LAST_KNOWN_API_VERSION)

LOG = logging.getLogger(__name__)
USER_AGENT = 'python-flocxclient'

_MAJOR_VERSION = 1
API_VERSION = '/v%d' % _MAJOR_VERSION
API_VERSION_SELECTED_STATES = ('user', 'negotiated', 'cached', 'default')


DEFAULT_MAX_RETRIES = 0
DEFAULT_RETRY_INTERVAL = 2

SUPPORTED_ENDPOINT_SCHEME = ('http', 'https')


class SessionClient(adapter.LegacyJsonAdapter):
    """HTTP client based on Keystone client session."""

    def __init__(self,
                 os_flocx_api_version,
                 **kwargs):
        self.os_flocx_api_version = os_flocx_api_version

        super(SessionClient, self).__init__(**kwargs)

        endpoint = self.get_endpoint()

        if endpoint is None:
            # placeholder for actual error handling
            raise Exception('The Market API endpoint cannot be detected and '
                            'was not provided explicitly')

    def _http_request(self, url, method, **kwargs):

        kwargs.setdefault('user_agent', USER_AGENT)
        kwargs.setdefault('auth', self.auth)

        if getattr(self, 'os_flocx_api_version', None):
            kwargs['headers'].setdefault('X-OpenStack-Flocx-API-Version',
                                         self.os_flocx_api_version)

        endpoint_filter = kwargs.setdefault('endpoint_filter', {})
        endpoint_filter.setdefault('interface', self.interface)
        endpoint_filter.setdefault('service_type', self.service_type)
        endpoint_filter.setdefault('region_name', self.region_name)

        resp = self.session.request(url, method,
                                    raise_exc=False, **kwargs)

        return resp

    def json_request(self, method, url, **kwargs):

        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type', 'application/json')
        kwargs['headers'].setdefault('Accept', 'application/json')

        if 'body' in kwargs:
            kwargs['data'] = jsonutils.dump_as_bytes(kwargs.pop('body'))

        resp = self._http_request(url, method, **kwargs)

        body = resp.content
        content_type = resp.headers.get('content-type', None)

        status = resp.status_code
        if (status in (http_client.NO_CONTENT, http_client.RESET_CONTENT)
                or content_type is None):
            return resp, list()

        if 'application/json' in content_type:

            try:
                body = resp.json()
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body


def _construct_http_client(session,
                           os_flocx_api_version=DEFAULT_VER,
                           **kwargs):

    kwargs.setdefault('service_type', 'market')
    kwargs.setdefault('user_agent', 'python-flocxclient')
    kwargs.setdefault('interface', kwargs.pop('endpoint_type',
                                              'publicURL'))

    return SessionClient(os_flocx_api_version=os_flocx_api_version,
                         session=session,
                         **kwargs
                         )
