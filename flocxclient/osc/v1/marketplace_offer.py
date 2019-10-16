import logging

from osc_lib.command import command
from osc_lib import utils as oscutils

from flocxclient.v1 import resource_fields as res_fields

LOG = logging.getLogger(__name__)


class ListOffers(command.Lister):

    def get_parser(self, prog_name):

        parser = super(ListOffers, self).get_parser(prog_name)

        parser.add_argument(
            '--limit',
            metavar='<limit>',
            type=int,
            help="""Maximum number of offers to return per request
                    0 for no limit. Default is the maximum number used
                    by the Marketplace API Service.""")
        parser.add_argument(
            '--offer-state',
            dest='provision_state',
            metavar='<provision state>',
            help="""List nodes in specified provision state.""")
        parser.add_argument(
            '--resource-class',
            dest='resource_class',
            metavar='<resource class>',
            help="Limit list to nodes with resource class <resource class>")
        parser.add_argument(
            '--owner',
            metavar='<owner>',
            help=""""Limit list to nodes with owner <owner>""")

        return parser

    def take_action(self, parsed_args):

        client = self.app.client_manager.market
        data = client.offer.list()

        columns = res_fields.OFFER_RESOURCE.fields
        labels = res_fields.OFFER_RESOURCE.labels

        return (labels,
                (oscutils.get_item_properties(s, columns) for s in data))
