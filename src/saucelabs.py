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

import base64
import json
import unittest
import sys

import requests


USER_NAME = 'valermor'
ACCESS_KEY = '764435f9-7986-4878-b6c8-8a100fda8cba'


class SauceLabsTestConfig():
    """
    This class exposes all the primitives needed to configure saucelabs test runs.
    """

    def __init__(self):
        self.grid_url = "https://saucelabs.com/"
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


class SkipTest(Exception):
    """
    Raise this exception in a test to skip it.

    Usually you can use TestCase.skipTest() or one of the skipping decorators
    instead of raising this directly.
    """
    pass


class SaucelabsReportingTestCase(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(SaucelabsReportingTestCase, self).__init__(methodName)
        self.driver = None
        self.config = SauceLabsTestConfig()

    def set_driver(self, driver):
        self.driver = driver

    def run(self, result=None):
        orig_result = result
        if result is None:
            result = self.defaultTestResult()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()

        self._resultForDoCleanups = result
        result.startTest(self)

        testMethod = getattr(self, self._testMethodName)
        if (getattr(self.__class__, "__unittest_skip__", False) or
            getattr(testMethod, "__unittest_skip__", False)):
            # If the class or method was skipped.
            try:
                skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                            or getattr(testMethod, '__unittest_skip_why__', ''))
                self._addSkip(result, skip_why)
            finally:
                result.stopTest(self)
            return
        try:
            success = False
            try:
                self.setUp()
            except SkipTest as e:
                self._addSkip(result, str(e))
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
            else:
                try:
                    self.config.start(self)
                    testMethod()
                except KeyboardInterrupt:
                    raise
                except self.failureException:
                    result.addFailure(self, sys.exc_info())
                    self.config.fail()
                except SkipTest as e:
                    self._addSkip(result, str(e))
                except:
                    result.addError(self, sys.exc_info())
                    self.config.fail()
                else:
                    success = True
                try:
                    self.tearDown()
                except KeyboardInterrupt:
                    raise
                except:
                    result.addError(self, sys.exc_info())
                    success = False

            cleanUpSuccess = self.doCleanups()
            success = success and cleanUpSuccess
            if success:
                result.addSuccess(self)
                self.config.success()
        finally:
            result.stopTest(self)
            if orig_result is None:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
