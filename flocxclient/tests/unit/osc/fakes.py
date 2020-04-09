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


# A random explicit version
API_VERSION = '1.0'


class FakeClientManager(object):
    def __init__(self):
        self.identity = None
        self.auth_ref = None
        self.interface = 'public'
        self._region_name = 'RegionOne'
        self.session = 'fake session'
        self._api_version = {'market': API_VERSION}


class FakeResource(object):
    def __init__(self, manager, info):
        self.__name__ = type(self).__name__
        self.manager = manager
        self._info = info
        self._add_details(info)

    def _add_details(self, info):
        for (k, v) in info.items():
            setattr(self, k, v)
