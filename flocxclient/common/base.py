"""
Base utilities to build API operation managers and objects on top of.
"""

import copy
import logging
import abc
import six

from flocxclient.common.apiclient import base


LOG = logging.getLogger(__name__)


def getid(obj):
    """Wrapper to get  object's ID.
    Abstracts the common pattern of allowing both an object or an
    object's ID (UUID) as a parameter when dealing with relationships.
    """
    try:
        return obj.id
    except AttributeError:
        return obj


@six.add_metaclass(abc.ABCMeta)
class Manager(object):
    """Provides  CRUD operations with a particular API."""

    @property
    @abc.abstractmethod
    def resource_class(self):
        """The resource class
        """

    @property
    @abc.abstractmethod
    def _resource_name(self):
        """The resource name.
        """

    def __init__(self, api):
        self.api = api

    def _path(self, resource_id=None):
        """Returns a request path for a given resource identifier.
        :param resource_id: Identifier of the resource to generate the request
                            path.
        """

        # NOTE: currently the flocx-market service does not use versioned urls
        # The below snippet would be correct if flocx-market used proper urls
        # return ('/v1/%s/%s' % (self._resource_name, resource_id)
        #          if resource_id else '/v1/%s' % self._resource_name)

        return ('/%s/%s' % (self._resource_name, resource_id)
                if resource_id else '/%s' % self._resource_name)

    def _get(self, resource_id, fields=None, os_flocx_api_version=None):
        """Retrieve a resource.
        :param resource_id: Identifier of the resource.
        :param fields: List of specific fields to be returned.
        :param os_flocx_api_version: String version (e.g. "1.35") to use for
            the request.  If not specified, the client's default is used.
        :raises exc.ValidationError: For invalid resource_id arg value.
        """

        if not resource_id:
            raise Exception("The identifier argument is invalid. Value "
                            "provided: {!r}".format(resource_id))

        if fields is not None:
            resource_id = '%s?fields=' % resource_id
            resource_id += ','.join(fields)

        try:
            return self._list(
                self._path(resource_id),
                os_flocx_api_version=os_flocx_api_version)[0]
        except IndexError:
            return None

    def _get_as_dict(self, resource_id, fields=None,
                     os_flocx_api_version=None):
        """Retrieve a resource as a dictionary
        :param resource_id: Identifier of the resource.
        :param fields: List of specific fields to be returned.
        :param os_flocx_api_version: String version (e.g. "1.35") to use for
            the request.  If not specified, the client's default is used.
        :returns: a dictionary representing the resource; may be empty
        """

        resource = self._get(resource_id, fields=fields,
                             os_flocx_api_version=os_flocx_api_version)
        if resource:
            return resource.to_dict()
        else:
            return {}

    def _format_body_data(self, body, response_key):

        if response_key:
            try:
                # there is no error handling if the body returns none
                data = body[response_key]
            except KeyError:
                LOG.warning("end _format_body_data through []")
                return []
        else:
            data = body

        if not isinstance(data, list):
            data = [data]

        return data

    def __list(self, url, response_key=None, body=None,
               os_flocx_api_version=None):
        kwargs = {}

        if os_flocx_api_version is not None:
            kwargs['headers'] = {'X-OpenStack-Flocx-API-Version':
                                 os_flocx_api_version}

        resp, body = self.api.json_request('GET', url, **kwargs)

        data = self._format_body_data(body, response_key)

        return data

    def _list(self, url, response_key=None, obj_class=None, body=None,
              os_flocx_api_version=None):
        if obj_class is None:
            obj_class = self.resource_class

        data = self.__list(url, response_key=response_key, body=body,
                           os_flocx_api_version=os_flocx_api_version)

        return [obj_class(self, res, loaded=True) for res in data if res]

    def _list_primitives(self, url, response_key=None):
        return self.__list(url, response_key=response_key)


@six.add_metaclass(abc.ABCMeta)
class CreateManager(Manager):
    """Provides creation operations with a particular API."""

    @property
    @abc.abstractmethod
    def _creation_attributes(self):
        """A list of required creation attributes for a resource type.
        """

    def create(self, **kwargs):
        """Create a resource based on a kwargs dictionary of attributes.
        :param kwargs: A dictionary containing the attributes of the resource
                       that will be created.
        :raises exc.InvalidAttribute: For invalid attributes that are not
                                      needed to create the resource.
        """

        new = {}
        invalid = []
        for (key, value) in kwargs.items():
            if key in self._creation_attributes:
                new[key] = value
            else:
                invalid.append(key)
        if invalid:
            Exception('The attribute(s) "%(attrs)s" are invalid; they '
                      'are not needed to create %(resource)s.' %
                      {'resource': self._resource_name,
                       'attrs': '","'.join(invalid)})
        url = self._path()
        resp, body = self.api.json_request('POST', url, body=new)
        if body:
            return self.resource_class(self, body)


class Resource(base.Resource):
    """Represents a particular instance of an object (tenant, user, etc).
    This is pretty much just a bag for attributes.
    """

    def to_dict(self):
        return copy.deepcopy(self._info)
