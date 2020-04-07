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


class Resource(object):
    """Base class for OpenStack resources (tenant, user, etc.).
    This is pretty much just a bag for attributes.
    """

    def __init__(self, manager, info):
        """Populate and bind to a manager.
        :param manager: BaseManager object
        :param info: dictionary representing resource attributes
        """
        self.manager = manager
        self._info = info
        self._add_details(info)

    def _add_details(self, info):
        for (k, v) in info.items():
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass
