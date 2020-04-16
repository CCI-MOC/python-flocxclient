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

from flocxclient.common import base

LOG = logging.getLogger(__name__)


class Offer(base.Resource):
    def __repr__(self):
        return "<Offer %s>" % self._info


class OfferManager(base.Manager):
    resource_class = Offer
    _creation_attributes = ['provider_offer_id', 'status',
                            'project_id', 'server_id', 'start_time',
                            'end_time', 'server_config', 'cost']
    _resource_name = 'offer'

    def list(self, os_flocx_api_version=None):
        """Retrieve a list of offers.
        :returns: A list of offers.
        """

        path = ''
        offers = self._list(self._path(path),
                            os_flocx_api_version=os_flocx_api_version)

        return offers

    def get(self, offer_id):
        """Get an offer with the specified identifier.
        :param offer_id: The UUID or name of an allocation.
        :returns: a :class:`Offer` object.
        """

        offer = self._get(resource_id=offer_id)

        return offer

    def create(self, **kwargs):
        """Create an offer based on a kwargs dictionary of attributes.
        :returns: a :class: `Offer` object
        """

        offer = self._create(**kwargs)

        return offer
