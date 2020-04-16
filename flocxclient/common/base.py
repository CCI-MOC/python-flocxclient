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

"""
Base utilities to build API operation managers and objects on top of.
"""

import logging
import abc
import six

from flocxclient.common.apiclient import base


LOG = logging.getLogger(__name__)


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

    @property
    @abc.abstractmethod
    def _creation_attributes(self):
        """A list of required creation attributes for a resource type.
        """

    def __init__(self, api):
        self.api = api

    def _path(self, resource_id=None):
        """Returns a request path for a given resource identifier.
        :param resource_id: Identifier of the resource to generate the request
                            path.
        """

        # NOTE: currently the flocx-market service does not use versioned urls
        # The below snippet would be correct if
        # flocx-market used versioned urls
        # return ('/v1/%s/%s' % (self._resource_name, resource_id)
        #          if resource_id else '/v1/%s' % self._resource_name)

        return ('/%s/%s' % (self._resource_name, resource_id)
                if resource_id else '/%s' % self._resource_name)

    def _get(self, resource_id, os_flocx_api_version=None):
        """Retrieve a resource.
        :param resource_id: Identifier of the resource.
        :param os_flocx_api_version: String version (e.g. "1.35") to use for
            the request.  If not specified, the client's default is used.
        :raises exc.ValidationError: For invalid resource_id arg value.
        """

        if not resource_id:
            raise Exception(
                "The identifier argument is invalid. "
                "Value provided: {!r}".format(resource_id))

        try:
            return self._list(
                self._path(resource_id),
                os_flocx_api_version=os_flocx_api_version)[0]
        except IndexError:
            return None

    def _format_body_data(self, body):

        data = body

        if not isinstance(data, list):
            data = [data]

        return data

    def _list(self, url, obj_class=None, os_flocx_api_version=None):
        if obj_class is None:
            obj_class = self.resource_class

        kwargs = {}

        if os_flocx_api_version is not None:
            kwargs['headers'] = {'X-OpenStack-Flocx-API-Version':
                                 os_flocx_api_version}

        resp, body = self.api.json_request('GET', url, **kwargs)

        data = self._format_body_data(body)

        return [obj_class(self, res) for res in data if res]

    def _create(self, **kwargs):
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
            raise Exception('The attribute(s) "%(attrs)s" '
                            'are invalid; they are not '
                            'needed to create %(resource)s.' %
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
