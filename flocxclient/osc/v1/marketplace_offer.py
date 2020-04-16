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
import json

from osc_lib.command import command
from osc_lib import utils as oscutils

from flocxclient.v1 import resource_fields as res_fields

LOG = logging.getLogger(__name__)


class CreateMarketOffer(command.ShowOne):
    """Create a new market offer."""

    log = logging.getLogger(__name__ + ".CreateMarketOffer")

    def get_parser(self, prog_name):
        parser = super(CreateMarketOffer, self).get_parser(prog_name)

        parser.add_argument(
            '--cost',
            dest='cost',
            required=True,
            help="Cost of the offer.")

        parser.add_argument(
            '--provider-offer-id',
            dest='provider_offer_id',
            required=True,
            help="Offer ID in the provider's database.")
        parser.add_argument(
            '--status',
            dest='status',
            required=True,
            help='State which the offer should be created in.')
        parser.add_argument(
            '--project-id',
            dest='project_id',
            required=True,
            help='Project ID of provider creating this offer.')
        parser.add_argument(
            '--server-id',
            dest='server_id',
            required=True,
            help='Name of the server being put into the offer.')
        parser.add_argument(
            '--start-time',
            dest='start_time',
            required=True,
            help="Time when the offer will be made 'available'.")
        parser.add_argument(
            '--end-time',
            dest='end_time',
            required=True,
            help="Time when the offer will expire and no longer be "
                 "'available'.")
        parser.add_argument(
            '--server-config',
            dest='server_config',
            required=True,
            help="Record arbitrary key/value server configuration "
                 "information. Pass in as a json object.")

        return parser

    def take_action(self, parsed_args):

        market_client = self.app.client_manager.market

        field_list = ['provider_offer_id', 'status', 'project_id', 'server_id',
                      'start_time', 'end_time', 'server_config', 'cost']

        fields = dict((k, v) for (k, v) in vars(parsed_args).items()
                      if k in field_list and v is not None)

        fields['server_config'] = json.loads(fields['server_config'])
        fields['cost'] = float(fields['cost'])

        offer = market_client.offer.create(**fields)

        data = dict([(f, getattr(offer, f, '')) for f in
                    res_fields.OFFER_RESOURCE.fields])

        return self.dict2columns(data)


class ShowMarketOffer(command.ShowOne):
    """Show market offer details."""

    log = logging.getLogger(__name__ + ".ShowMarketOffer")

    def get_parser(self, prog_name):
        parser = super(ShowMarketOffer, self).get_parser(prog_name)
        parser.add_argument(
            "id",
            metavar="<id>",
            help="Offer ID of the offer")

        return parser

    def take_action(self, parsed_args):

        market_client = self.app.client_manager.market

        offer = market_client.offer.get(parsed_args.id)

        offer = offer._info
        return zip(*sorted(offer.items()))


class ListMarketOffer(command.Lister):
    """List market offers."""

    def get_parser(self, prog_name):

        parser = super(ListMarketOffer, self).get_parser(prog_name)

        return parser

    def take_action(self, parsed_args):

        market_client = self.app.client_manager.market
        data = market_client.offer.list()
        columns = res_fields.OFFER_RESOURCE.fields
        labels = res_fields.OFFER_RESOURCE.labels

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))
