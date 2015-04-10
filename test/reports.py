import os
import re

from galenapi.galen_api import generate_galen_report


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
