import testtools

from flocxclient.tests.unit import utils
from flocxclient.tests.unit.osc.fakes import FakeResource

import flocxclient.v1.offer


OFFER = {
    'cost': "1000",
    'created_at': '2000-00-00T13',
    'end_time': "3000-00-00T13",
    'marketplace_offer_id': "wwwwwwww-wwww-wwww-wwww-wwwwwwwwwwww",
    'project_id': "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    'provider_offer_id': "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
    'server_config': {},
    'server_id': "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
    'start_time': "2010",
    'status': "fake_status",
    'updated_at': None
}

OFFER2 = {
    'cost': "20.0",
    'created_at': '2020-08-20T13',
    'end_time': "2020-07-24T13",
    'marketplace_offer_id': "2222222222",
    'project_id': "1",
    'provider_offer_id': "2",
    'server_config': {},
    'server_id': "101010",
    'start_time': "2019",
    'status': "available",
    'updated_at': None
}


fake_responses = {
    '/offer':
    {
        'GET': (
            {},
            [OFFER, OFFER2],
        ),
    },

}


class OfferManagerTest(testtools.TestCase):

    def setUp(self):
        super(OfferManagerTest, self).setUp()
        self.api = utils.FakeAPI(fake_responses)
        self.mgr = flocxclient.v1.offer.OfferManager(self.api)

    def test_offers_list(self):
        resources_list = self.mgr.list()
        expect = [
            ('GET', '/offer', {}, None),
        ]
        self.assertEqual(expect, self.api.calls)

        expected_resp = ({}, [OFFER, OFFER2],)
        expected_resources = [FakeResource(None, OFFER),
                              FakeResource(None, OFFER2)]

        self.assertEqual(expected_resp, self.api.responses['/offer']['GET'])
        assert (len(expected_resources) == 2)
        self.assertEqual(resources_list[0]._info, expected_resources[0]._info)
        self.assertEqual(resources_list[1]._info, expected_resources[1]._info)
