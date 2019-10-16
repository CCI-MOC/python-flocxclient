import logging


from flocxclient.common import http
from flocxclient.v1 import offer


LOG = logging.getLogger(__name__)


class Client(object):
    """Client for the Flocx v1 API.
    :param string endpoint_override: A user-supplied endpoint URL for the
                                     flocx service.
    :param session: A keystoneauth Session object (must be provided as
        a keyword argument).
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Flocx v1 API."""

        self.http_client = http._construct_http_client(*args, **kwargs)
        self.offer = offer.OfferManager(self.http_client)

    @property
    def current_api_version(self):
        """Return the current API version in use.
        This returns the version of the REST API that the API client
        is presently set to request. This value may change as a result
        of API version negotiation.
        """
        return self.http_client.os_flocx_api_version
