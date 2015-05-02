import base64
import json
import os

from nose2.events import Plugin

import requests


USER_NAME = 'valermor'
ACCESS_KEY = '764435f9-7986-4878-b6c8-8a100fda8cba'


class SauceLabsTestConfig():
    """
    This class exposes all the primitives needed to configure saucelabs test runs.
    """

    def __init__(self, grid_url):
        self.grid_url = grid_url
        self.session_id = None

    def start(self, testcase):
        """
        Initializes a test run with the complete name of the test case.
        Further info at https://docs.saucelabs.com/reference/test-configuration/
        """
        body_content = json.dumps({"name": str(testcase)})
        self.session_id = testcase.driver.session_id
        return self.__put_info(body_content)

    def fail(self):
        """
        Marks executed test as failed.
        """
        self._send_pass_status(False)

    def success(self):
        """
        Marks executed test as passed.
        """
        self._send_pass_status(True)

    def _send_pass_status(self, status):
        body_content = json.dumps({"passed": status})
        return self.__put_info(body_content)

    def __put_info(self, body):
        base64string = base64.encodestring('%s:%s' % (USER_NAME, ACCESS_KEY))[:-1]
        put_url = self.grid_url + "/rest/v1/{user_name}/jobs/{session_id}".format(user_name=USER_NAME, session_id=self.session_id)
        headers = {"Authorization": "Basic %s" % base64string}
        request = requests.put(put_url, headers=headers, data=body)

        return request.status_code == requests.codes.ok


class SaucelabsPlugin(Plugin):
    """
    Report into Saucelabs details about execution of tests.
    """
    configSection = 'saucelabs'
    commandLineSwitch = (None, 'saucelabs', 'Sends test configuration info to Saucelabs')

    def __init__(self):
        self.config = SauceLabsTestConfig(os.getenv('GRID_URL'))

    def startTest(self, event):
        self.config.start(str(event.test))

    def reportSuccess(self, event):
        self.config.success()

    def reportFailure(self, event):
        self.config.fail()

    def reportError(self, event):
        self.config.fail()

