import logging
import re

from keystoneauth1 import adapter
from oslo_serialization import jsonutils


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

_API_VERSION_RE = re.compile(r'/+(v%d)?/*$' % _MAJOR_VERSION)


def _trim_endpoint_api_version(url):
    """Trim API version and trailing slash from endpoint."""
    return re.sub(_API_VERSION_RE, '', url)


def _extract_error_json(body):
    """Return  error_message from the HTTP response body."""
    try:
        body_json = jsonutils.loads(body)
    except ValueError:
        return {}

    if 'error_message' not in body_json:
        return {}

    try:
        error_json = jsonutils.loads(body_json['error_message'])
    except ValueError:
        return body_json

    err_msg = (error_json.get('faultstring') or error_json.get('description'))
    if err_msg:
        body_json['error_message'] = err_msg

    return body_json


class SessionClient(adapter.LegacyJsonAdapter):
    """HTTP client based on Keystone client session."""

    def __init__(self,
                 os_flocx_api_version,
                 api_version_select_state,
                 max_retries,
                 retry_interval,
                 **kwargs):
        self.os_flocx_api_version = os_flocx_api_version
        self.api_version_select_state = api_version_select_state
        self.conflict_max_retries = max_retries
        self.conflict_retry_interval = retry_interval
        if isinstance(kwargs.get('endpoint_override'), str):
            kwargs['endpoint_override'] = _trim_endpoint_api_version(
                kwargs['endpoint_override'])

        super(SessionClient, self).__init__(**kwargs)

        endpoint_filter = self._get_endpoint_filter()
        endpoint = self.get_endpoint(**endpoint_filter)
        if endpoint is None:
            # placeholder for actual error handling
            raise Exception('The Market API endpoint cannot be detected and '
                            'was not provided explicitly')

        self.endpoint_trimmed = _trim_endpoint_api_version(endpoint)

    def _parse_version_headers(self, resp):
        return self._generic_parse_version_headers(resp.headers.get)

    def _get_endpoint_filter(self):
        return {
            'interface': self.interface,
            'service_type': self.service_type,
            'region_name': self.region_name
        }

    def _make_simple_request(self, conn, method, url):
        # NOTE: conn is self.session for this class
        return conn.request(url, method, raise_exc=False,
                            user_agent=USER_AGENT,
                            endpoint_filter=self._get_endpoint_filter(),
                            endpoint_override=self.endpoint_override)

    def _http_request(self, url, method, **kwargs):

        kwargs.setdefault('user_agent', USER_AGENT)
        kwargs.setdefault('auth', self.auth)
        if isinstance(self.endpoint_override, str):
            kwargs.setdefault('endpoint_override', self.endpoint_override)

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

        if 'application/json' in content_type:
            try:
                body = resp.json()
            except ValueError:
                LOG.error('Could not decode response body as JSON')
        else:
            body = None

        return resp, body

    def raw_request(self, method, url, **kwargs):
        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Content-Type',
                                     'application/octet-stream')
        return self._http_request(url, method, **kwargs)


def _construct_http_client(session,
                           os_flocx_api_version=DEFAULT_VER,
                           api_version_select_state='default',
                           max_retries=DEFAULT_MAX_RETRIES,
                           retry_interval=DEFAULT_RETRY_INTERVAL,
                           **kwargs):

    kwargs.setdefault('service_type', 'market')
    kwargs.setdefault('user_agent', 'python-flocxclient')
    kwargs.setdefault('interface', kwargs.pop('endpoint_type',
                                              'publicURL'))

    return SessionClient(os_flocx_api_version=os_flocx_api_version,
                         api_version_select_state=api_version_select_state,
                         max_retries=max_retries,
                         retry_interval=retry_interval,
                         session=session,
                         **kwargs
                         )
