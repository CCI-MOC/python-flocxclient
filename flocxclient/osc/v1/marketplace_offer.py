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

from osc_lib.command import command
from osc_lib import utils as oscutils

from flocxclient.v1 import resource_fields as res_fields

LOG = logging.getLogger(__name__)


class ListMarketOffer(command.Lister):

    def get_parser(self, prog_name):

        parser = super(ListMarketOffer, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.market
        data = client.offer.list()
        columns = res_fields.OFFER_RESOURCE.fields
        labels = res_fields.OFFER_RESOURCE.labels

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))
