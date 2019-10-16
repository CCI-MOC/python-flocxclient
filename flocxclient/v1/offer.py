import logging

from flocxclient.common import base

LOG = logging.getLogger(__name__)


class Offer(base.Resource):
    def __repr__(self):
        return "<Offer %s>" % self._info


class OfferManager(base.CreateManager):
    resource_class = Offer
    _creation_attributes = []
    _resource_name = 'offer'

    def list(self, os_flocx_api_version=None):
        """Retrieve a list of offers.
        :returns: A list of offers.
        """

        path = ''

        return self._list(self._path(path),
                          os_flocx_api_version=os_flocx_api_version)
