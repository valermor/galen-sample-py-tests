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

import os
import re

from galenpy.galen_api import generate_galen_report


PROJECT_NAME = 'galen-sample-py-tests'


def galen_report():
    generate_galen_report(get_target_dir(PROJECT_NAME, 'target/galen'))


def get_target_dir(project_name, target_dir):
    p = re.compile('(.*/' + project_name + ').*')
    m = p.match(os.getcwd())
    if m.groups():
        return os.path.join(m.groups()[0], target_dir)

if __name__ == '__main__':
    galen_report()
