############################################################################
# Copyright 2015 Valerio Morsella                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################

from nose2.tools import params

from src.devices import device_provider
from src.galen_test_base import GalenTestBase
from src.groups import groups
from src.pages import load_login_page, load_welcome_page


class DemoPageTest(GalenTestBase):

    @groups("LAYOUT")
    @params(*device_provider)
    def test_welcome_page_should_look_good_on_device(self, device):

        load_welcome_page(self.driver).for_screen_size(device.width, device.height)

        self.check_layout("welcome page for device " + device.name, "welcomePage.spec", device.included_tags, device.excluded_tags)

    @groups("LAYOUT")
    @params(*device_provider)
    def test_login_page_should_look_good_on_device(self, device):

        load_login_page(self.driver).for_screen_size(device.width, device.height)

        self.check_layout("login page for device " + device.name, "loginPage.spec", device.included_tags, device.excluded_tags)

