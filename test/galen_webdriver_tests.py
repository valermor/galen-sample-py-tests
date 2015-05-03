############################################################################
# Copyright 2015 Valerio Morsella                                          #
# #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
# #
#    http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import os
import unittest

from galenpy.galen_webdriver import GalenRemoteWebDriver
from hamcrest import assert_that, has_entry, equal_to, contains_string, has_item, less_than, calling, raises
from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.library.collection.isdict_containing import IsDictContaining
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from src.groups import groups
from src.saucelabs import SaucelabsReportingTestCase

DESIRED_CAPS = DesiredCapabilities.FIREFOX

class GalenWebDriverTest(SaucelabsReportingTestCase):

    def __init__(self, methodName='runTest'):
        super(GalenWebDriverTest, self).__init__(methodName)

    def setUp(self):
        self.set_driver(GalenRemoteWebDriver(remote_url=os.getenv('GRID_URL', 'http://127.0.0.1:4444/wd/hub'),
                                           desired_capabilities=DESIRED_CAPS))

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    @groups("WEBDRIVER")
    def test_can_get_capabilities(self):
        """
        Checks that GalenRemoteWebDriver can receive capabilities with right type.
        """
        caps = self.driver.capabilities
        assert_that(caps, has_entry('platform', 'LINUX'), 'should contain a string element')
        assert_that(caps, has_entry('webdriver.remote.sessionid', self.driver.session_id),
                    'should contain a string element')
        assert_that(caps, has_entry('browserName', DESIRED_CAPS['browserName']), 'should contain a string element')
        assert_that(caps, has_entry('nativeEvents', True), 'should contain a bool element')
        assert_that(caps, has_entry('takesScreenshot', True), 'should contain a bool element')
        assert_that(caps, has_entry_containing_dict_with_key('chrome'), 'should contain a dict element')

    @groups("WEBDRIVER")
    def test_can_get_title(self):
        self.load_test_page()
        assert_that(self.driver.title, 'Sample Website For Galen Framework')

    @groups("WEBDRIVER")
    def test_can_find_element(self):
        self.load_test_page()
        login_button = self.driver.find_element_by_css_selector(".button-login")
        assert_that(type(login_button), equal_to(WebElement), 'should be able to retrieve a WebElement')
        assert_that(login_button.text, equal_to('Login'))
        assert_that(login_button.get_attribute('type'), equal_to('button'))

    @groups("WEBDRIVER")
    def test_can_find_elements(self):
        self.load_test_page()
        elements = self.driver.find_elements_by_css_selector(".button-login")
        login_button = elements[0]
        assert_that(type(login_button), equal_to(WebElement), 'should be able to retrieve a WebElement')
        assert_that(login_button.text, equal_to('Login'))
        assert_that(login_button.get_attribute('type'), equal_to('button'))

    @groups("WEBDRIVER")
    def test_can_get_current_url(self):
        self.load_test_page()
        assert_that(self.driver.current_url, equal_to('http://testapp.galenframework.com/'))

    @groups("WEBDRIVER")
    def test_can_get_page_source(self):
        self.load_test_page()
        page_source = self.driver.page_source
        assert_that(page_source, contains_string('Sample Website'))
        assert_that(page_source, contains_string('for Galen Framework'))
        assert_that(page_source, contains_string('</html>'))

    @groups("WEBDRIVER")
    def test_can_get_current_window_handle(self):
        self.load_test_page()
        handle = self.driver.current_window_handle
        assert_that(type(handle), equal_to(str))

    @groups("WEBDRIVER")
    def test_can_get_window_handles(self):
        self.load_test_page()
        handles = self.driver.window_handles
        assert_that(handles, has_item(self.driver.current_window_handle))

    @groups("WEBDRIVER")
    def test_can_maximize_window(self):
        wait = WebDriverWait(self.driver, 25)
        self.load_test_page()
        self.driver.set_window_size(375, 667)
        wait.until(lambda x: windows_size_is(x, 375, 667), message="windows size should be 375x667")
        size_before = self.driver.get_window_size()
        self.driver.maximize_window()
        wait.until(lambda x: windows_size_greater_than(x, 375, 667), message="windows size should be greater 375x667")
        size_after = self.driver.get_window_size()
        assert_that(int(size_before['width']), less_than(int(size_after['width'])),
                    "screen width should be bigger after resizing")
        assert_that(int(size_before['height']), less_than(int(size_after['height'])),
                    "screen height should be bigger after resizing")

    @groups("WEBDRIVER")
    def test_can_refresh(self):
        self.load_test_page()
        self.driver.refresh()
        assert_that(self.driver.current_url, equal_to('http://testapp.galenframework.com/'))

    @groups("WEBDRIVER")
    def test_can_get_cookie(self):
        self.load_test_page()
        self.driver.execute_script("document.cookie='acookie=thecookie'")
        cookie_name = self.driver.get_cookie('acookie')
        assert_that(cookie_name['value'], equal_to('thecookie'))

    @unittest.skip('Issue #3 GalenWebDriver commands containing optional *args not correctly handled')
    @groups("WEBDRIVER")
    def test_can_set_script_timeout(self):
        self.load_test_page()
        self.driver.set_script_timeout(0)
        self.driver.execute_async_script('document.cookie')

    def test_can_set_page_load_timeout(self):
        pass

    @groups("WEBDRIVER")
    def test_can_set_window_size(self):
        self.load_test_page()
        self.driver.set_window_size(400, 1000)
        wait = WebDriverWait(self.driver, 30, 3)
        wait.until(lambda x: windows_size_is(x, 400, 1000), message="windows size should be 400x500")
        size = self.driver.get_window_size()
        assert_that(size['width'], equal_to(400), 'should have width set to 400')
        assert_that(size['height'], equal_to(1000), 'should have height set to 500')


    def test_can_set_window_position(self):
        pass

    def test_can_get_window_position(self):
        pass

    def test_can_get_orientation(self):
        pass

    def test_can_set_orientation(self):
        pass

    def test_can_get_log_types(self):
        pass

    def test_can_get_log_type(self):
        pass

    @unittest.skip('Need a proper fix to package unhandled error from Remote WebDriver to exception class')
    @groups("WEBDRIVER")
    def test_can_manage_unhandled_exception(self):
        self.driver.set_script_timeout(0)
        assert_that(calling(failing_call(self.driver)), raises(WebDriverException))

    @groups("WEBDRIVER")
    def test_can_raise_no_such_element_exception(self):
        self.load_test_page()
        self.driver.find_element_by_xpath("anonexistinglocator")

    def load_test_page(self):
        self.driver.get('http://testapp.galenframework.com')


def windows_size_is(driver, width, height):
    size = driver.get_window_size()
    return size['width'] == width and size['height'] == height

def windows_size_greater_than(driver, width, height):
    size = driver.get_window_size()
    return size['width'] > width and size['height'] > height


def failing_call(a_driver):
    a_driver.execute_async_script('document.cookie')


class IsDictContainingDictValue(IsDictContaining):
    def __init__(self, key_matcher):
        IsDictContaining.__init__(self, key_matcher, "")

    def _matches(self, dictionary):
        if hasmethod(dictionary, 'values'):
            for key in dictionary.keys():
                if self.key_matcher.matches(key):
                    return isinstance(dictionary[key], dict)
        return False

    def describe_to(self, description):
        description.append_text('a dictionary containing a dict value with key:').append_description_of(
            self.key_matcher)


def has_entry_containing_dict_with_key(key_match):
    return IsDictContainingDictValue(wrap_matcher(key_match))
