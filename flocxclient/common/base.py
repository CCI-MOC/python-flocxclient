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

    def _format_body_data(self, body, response_key):

        if response_key:
            try:
                # there is no error handling if the body returns none
                data = body[response_key]
            except KeyError:
                return []
        else:
            data = body

        if not isinstance(data, list):
            data = [data]

        return data

    def __list(self, url, response_key=None,
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

        data = self.__list(url, response_key=response_key,
                           os_flocx_api_version=os_flocx_api_version)

        return [obj_class(self, res) for res in data if res]


@six.add_metaclass(abc.ABCMeta)
class CreateManager(Manager):
    """Provides creation operations with a particular API."""

    @property
    @abc.abstractmethod
    def _creation_attributes(self):
        """A list of required creation attributes for a resource type.
        """


class Resource(base.Resource):
    """Represents a particular instance of an object (tenant, user, etc).
    This is pretty much just a bag for attributes.
    """
