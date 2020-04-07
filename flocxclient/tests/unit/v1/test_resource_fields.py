import testtools

from flocxclient.v1 import resource_fields


class ResourceTest(testtools.TestCase):
    def setUp(self):
        super(ResourceTest, self).setUp()
        self._saved_ids = resource_fields.Resource.FIELDS
        resource_fields.Resource.FIELDS = {
            'item1': 'ITEM1',
            '2nd_item': 'A second item',
            'item_3': 'Third item',
        }

    def tearDown(self):
        super(ResourceTest, self).tearDown()
        resource_fields.Resource.FIELDS = self._saved_ids

    def test_fields_single_value(self):
        # Make sure single value is what we expect
        foo = resource_fields.Resource(['item1'])
        self.assertEqual(('item1',), foo.fields)
        self.assertEqual(('ITEM1',), foo.labels)

    def test_fields_multiple_value_order(self):
        # Make sure order is maintained
        foo = resource_fields.Resource(['2nd_item', 'item1'])
        self.assertEqual(('2nd_item', 'item1'), foo.fields)
        self.assertEqual(('A second item', 'ITEM1'), foo.labels)

    def test_unknown_field_id(self):
        self.assertRaises(
            KeyError,
            resource_fields.Resource,
            ['item1', 'unknown_id'])
