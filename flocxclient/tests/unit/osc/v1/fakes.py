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
import json

from osc_lib.tests import utils

from flocxclient.tests.unit.osc import fakes


market_cost = "1000.0"
market_created_at = "2000-00-00T13"
market_end_time = "3000-00-00T13"
market_marketplace_offer_id = "wwwwwwww-wwww-wwww-wwww-wwwwwwwwwwww"
market_project_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
market_provider_offer_id = "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
market_server_config = "{}"
market_server_id = "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
market_start_time = "2010"
market_status = "fake_status"
market_updated_at = None

OFFER = {
    'cost': float(market_cost),
    'created_at': market_created_at,
    'end_time': market_end_time,
    'marketplace_offer_id': market_marketplace_offer_id,
    'project_id': market_project_id,
    'provider_offer_id': market_provider_offer_id,
    'server_config': json.loads(market_server_config),
    'server_id': market_server_id,
    'start_time': market_start_time,
    'status': market_status,
    'updated_at': market_updated_at
}


class TestMarket(utils.TestCommand):

    def setUp(self):
        super(TestMarket, self).setUp()

        self.app.client_manager.auth_ref = mock.Mock(auth_token="TOKEN")
        self.app.client_manager.market = mock.Mock()


class FakeMarketResource(fakes.FakeResource):

    def get_keys(self):
        return {'property': 'value'}
