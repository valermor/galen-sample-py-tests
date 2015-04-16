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
import unittest

from galenpy.galen_webdriver import GalenRemoteWebDriver
from hamcrest import assert_that, has_entry, equal_to, contains_string, has_item, greater_than, less_than
from hamcrest.core.helpers.hasmethod import hasmethod
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.library.collection.isdict_containing import IsDictContaining
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from src.groups import groups


class GalenWebDriverTest(unittest.TestCase):

    def setUp(self):
        self.driver = GalenRemoteWebDriver("http://localhost:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)

    def tearDown(self):
        self.driver.quit()

    @groups("WEBDRIVER")
    def test_can_get_capabilities(self):
        """
        Checks that GalenRemoteWebDriver can receive capabilities with right type.
        """
        caps = self.driver.capabilities
        assert_that(caps, has_entry('platform', 'MAC'), 'should contain a string element')
        assert_that(caps, has_entry('webdriver.remote.sessionid', self.driver.session_id), 'should contain a string element')
        assert_that(caps, has_entry('browserName', 'chrome'), 'should contain a string element')
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
        self.load_test_page()
        size_before = self.driver.get_window_size()
        self.driver.maximize_window()
        size_after = self.driver.get_window_size()
        assert_that(int(size_before['width']), less_than(int(size_after['width'])),
                    "screen width should be higher after resizing")
        assert_that(int(size_before['height']), less_than(int(size_after['height'])),
                    "screen heigth should be higher after resizing")

    def test_can_refresh(self):
        self.load_test_page()
        self.driver.refresh()
        assert_that(self.driver.current_url, equal_to('http://testapp.galenframework.com/'))

    def test_can_get_cookie(self):
        self.load_test_page()
        self.driver.execute_script("document.cookie='acookie=thecookie'")
        cookie_name = self.driver.get_cookie('acookie')
        assert_that(cookie_name['value'], equal_to('thecookie'))

    def test_can_set_script_timeout(self):
        pass

    def test_can_set_page_load_timeout(self):
        pass

    def test_can_set_window_size(self):
        pass

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

    def load_test_page(self):
        self.driver.get('http://testapp.galenframework.com')


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
        description.append_text('a dictionary containing a dict value with key:')        \
                    .append_description_of(self.key_matcher)        \

def has_entry_containing_dict_with_key(key_match):
    return IsDictContainingDictValue(wrap_matcher(key_match))

if __name__ == '__main__':
    driver = WebDriver("http://localhost:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.get('http://testapp.galenframework.com')
    driver.maximize_window()
    print ''
