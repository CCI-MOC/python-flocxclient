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
import requests


class FakeAPI(object):
    """
    Provides a fake HTTP client with canned responses
    keeps track of calls made """

    def __init__(self, responses, path_prefix=None):
        self.responses = responses
        self.calls = []
        self.path_prefix = path_prefix or ''

    def _request(self, method, url, headers=None, body=None, params=None):
        # url should always just be a path here, e.g. /offer
        url = self.path_prefix + url

        call = (method, url, headers or {}, body)
        if params:
            call += (params,)
        self.calls.append(call)
        return self.responses[url][method]

    def json_request(self, *args, **kwargs):
        response = self._request(*args, **kwargs)
        return FakeResponse(response[0]), response[1]


class FakeResponse(object):
    def __init__(self, headers, body=None, status=None,
                 request_headers={}):
        """Fake object to help testing.
        :param headers: dict representing HTTP response headers
        :param body: file-like object
        """
        self.headers = headers
        self.body = body
        self.status_code = status
        self.request = mock.Mock()
        self.request.headers = request_headers


def mockSessionResponse(headers, content=None, status_code=None,
                        request_headers={}):

    request = mock.Mock()
    request.headers = request_headers
    response = mock.Mock(headers=headers,
                         content=content,
                         status_code=status_code,
                         request=request)
    response.text = content

    return response


def mockSession(headers, content=None, status_code=None, version=None):
    session = mock.Mock(spec=requests.Session,
                        verify=False,
                        cert=('test_cert', 'test_key'))
    session.get_endpoint = mock.Mock(return_value='https://test')
    response = mockSessionResponse(headers, content, status_code, version)
    session.request = mock.Mock(return_value=response)

    return session
