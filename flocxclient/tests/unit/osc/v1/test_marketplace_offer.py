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

import copy
import json

from osc_lib.tests import utils as osctestutils

from flocxclient.osc.v1 import marketplace_offer
from flocxclient.tests.unit.osc.v1 import fakes as market_fakes


class TestMarketOffer(market_fakes.TestMarket):

    def setUp(self):
        super(TestMarketOffer, self).setUp()

        self.market_mock = self.app.client_manager.market
        self.market_mock.reset_mock()


class TestCreateMarketOffer(TestMarketOffer):

    def setUp(self):
        super(TestCreateMarketOffer, self).setUp()

        self.market_mock.offer.create.return_value = (
            market_fakes.FakeMarketResource(
                None,
                copy.deepcopy(market_fakes.OFFER)
            ))

        # Get the command object to test
        self.cmd = marketplace_offer.CreateMarketOffer(self.app, None)

    def test_market_offer_create(self):
        arglist = [
            '--provider-offer-id', market_fakes.market_provider_offer_id,
            '--status', market_fakes.market_status,
            '--project-id', market_fakes.market_project_id,
            '--server-id', market_fakes.market_server_id,
            '--start-time', market_fakes.market_start_time,
            '--end-time', market_fakes.market_end_time,
            '--server-config', market_fakes.market_server_config,
            '--cost', market_fakes.market_cost,
        ]

        verifylist = [
            ('provider_offer_id', market_fakes.market_provider_offer_id),
            ('status', market_fakes.market_status),
            ('project_id', market_fakes.market_project_id),
            ('server_id', market_fakes.market_server_id),
            ('start_time', market_fakes.market_start_time),
            ('end_time', market_fakes.market_end_time),
            ('server_config', market_fakes.market_server_config),
            ('cost', market_fakes.market_cost),
        ]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        self.cmd.take_action(parsed_args)

        args = {
            'cost': float(market_fakes.market_cost),
            'provider_offer_id': market_fakes.market_provider_offer_id,
            'status': market_fakes.market_status,
            'project_id': market_fakes.market_project_id,
            'server_id': market_fakes.market_server_id,
            'start_time': market_fakes.market_start_time,
            'end_time': market_fakes.market_end_time,
            'server_config': json.loads(market_fakes.market_server_config),
        }

        self.market_mock.offer.create.assert_called_once_with(**args)


class TestMarketOfferList(TestMarketOffer):
    def setUp(self):
        super(TestMarketOfferList, self).setUp()

        self.market_mock.offer.list.return_value = [
            market_fakes.FakeMarketResource(
                None,
                copy.deepcopy(market_fakes.OFFER))
        ]
        self.cmd = marketplace_offer.ListMarketOffer(self.app, None)

    def test_market_offer_list(self):
        arglist = []
        verifylist = []

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.market_mock.offer.list.assert_called_with()

        collist = (
                "Cost",
                "Created At",
                "End Time",
                "Marketplace Offer ID",
                "Project ID",
                "Provider Offer ID",
                "Server Config",
                "Server ID",
                "Start Time",
                "Status",
                "Updated At"
        )
        self.assertEqual(collist, columns)

        datalist = ((float(market_fakes.market_cost),
                     market_fakes.market_created_at,
                     market_fakes.market_end_time,
                     market_fakes.market_marketplace_offer_id,
                     market_fakes.market_project_id,
                     market_fakes.market_provider_offer_id,
                     json.loads(market_fakes.market_server_config),
                     market_fakes.market_server_id,
                     market_fakes.market_start_time,
                     market_fakes.market_status,
                     market_fakes.market_updated_at
                     ),)
        self.assertEqual(datalist, tuple(data))


class TestMarketOfferShow(TestMarketOffer):
    def setUp(self):
        super(TestMarketOfferShow, self).setUp()

        self.market_mock.offer.get.return_value = market_fakes.\
            FakeMarketResource(None, copy.deepcopy(market_fakes.OFFER))

        self.cmd = marketplace_offer.ShowMarketOffer(self.app, None)

    def test_market_offer_show(self):
        arglist = [market_fakes.market_marketplace_offer_id]
        verifylist = [('id', market_fakes.market_marketplace_offer_id)]

        parsed_args = self.check_parser(self.cmd, arglist, verifylist)
        columns, data = self.cmd.take_action(parsed_args)

        self.market_mock.offer.get.assert_called_once_with(
            market_fakes.market_marketplace_offer_id)

        collist = (
                "cost",
                "created_at",
                "end_time",
                "marketplace_offer_id",
                "project_id",
                "provider_offer_id",
                "server_config",
                "server_id",
                "start_time",
                "status",
                "updated_at"
        )
        self.assertEqual(collist, columns)

        datalist = (float(market_fakes.market_cost),
                    market_fakes.market_created_at,
                    market_fakes.market_end_time,
                    market_fakes.market_marketplace_offer_id,
                    market_fakes.market_project_id,
                    market_fakes.market_provider_offer_id,
                    json.loads(market_fakes.market_server_config),
                    market_fakes.market_server_id,
                    market_fakes.market_start_time,
                    market_fakes.market_status,
                    market_fakes.market_updated_at
                    )
        self.assertEqual(datalist, tuple(data))

    def test_baremetal_allocation_show_no_id(self):
        arglist = []
        verifylist = []
        self.assertRaises(osctestutils.ParserException,
                          self.check_parser,
                          self.cmd, arglist, verifylist)
