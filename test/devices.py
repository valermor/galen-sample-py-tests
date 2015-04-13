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

class DeviceConfig(object):

    def __init__(self, name, width, height, included_tags, excluded_tags, enabled):
        self.name = name
        self.width = width
        self.height = height
        self.included_tags = included_tags
        self.excluded_tags = excluded_tags
        self.enabled = enabled

    def __str__(self):
        return "name: " + self.name + "\n" +\
               "width: " + self.width + "\n" +\
               "height: " + self.height + "\n" +\
               "included tags: " + str(self.included_tags) + "\n" +\
               "excluded tags: " + str(self.excluded_tags) + "\n"

PHONE = DeviceConfig("mobile", "450", "800", ["mobile"], None, True)
TABLET = DeviceConfig("tablet", "750", "800", ["tablet"], None, True)
DESKTOP = DeviceConfig("desktop", "1024", "800", ["desktop"], None, True)

all_devices = [PHONE, TABLET, DESKTOP]

device_provider = tuple(filter(lambda x: x.enabled, all_devices))
