class Resource(object):
    """Resource class
    This class is used to manage the various fields that a resource (e.g.
    Chassis, Node, Port) contains.  An individual field consists of a
    'field_id' (key) and a 'label' (value).  The caller only provides the
    'field_ids' when instantiating the object.
    Ordering of the 'field_ids' will be preserved as specified by the caller.
    It also provides the ability to exclude some of these fields when they are
    being used for sorting.
    """

    FIELDS = {
        'created_at': "Created At",
        'updated_at': "Updated At",
        'marketplace_offer_id': "Marketplace Offer ID",
        'provider_offer_id': "Provider Offer ID",
        'project_id': "Project ID",
        'status': "Status",
        'server_id': "Server ID",
        'start_time': "Start Time",
        'end_time': "End Time",
        'server_config': "Server Config",
        'cost': "Cost"
    }

    def __init__(self, field_ids):
        """Create a Resource object
        :param field_ids:  A list of strings that the Resource object will
                           contain.  Each string must match an existing key in
                           FIELDS.
        :raises: ValueError if sort_excluded or override_labels contains values
                 not in field_ids
        """

        self._fields = tuple(field_ids)
        self._labels = tuple([self.FIELDS[x] for x in field_ids])

        self._sort_fields = tuple(
            [x for x in field_ids])

    @property
    def fields(self):
        return self._fields

    @property
    def labels(self):
        return self._labels

    @property
    def sort_fields(self):
        return self._sort_fields


OFFER_RESOURCE = Resource(
    ['cost',
     'created_at',
     'end_time',
     'marketplace_offer_id',
     'project_id',
     'provider_offer_id',
     'server_config',
     'server_id',
     'start_time',
     'status',
     'updated_at'])
