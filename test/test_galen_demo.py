from nose2.tools import params

from test.devices import device_provider

from test.galen_test_base import GalenTestBase
from test.groups import groups


class WelcomePageTest(GalenTestBase):

    @groups("LAYOUT")
    @params(*device_provider)
    def test_welcome_page_should_look_good_on_device(self, device):
        self.load("http://testapp.galenframework.com", device.width, device.height)
        self.check_layout("welcome page", "welcomePage.spec", device.included_tags, device.excluded_tags)

    @groups("LAYOUT")
    @params(*device_provider)
    def test_login_page_should_look_good_on_device(self, device):
        self.load("http://testapp.galenframework.com", device.width, device.height)
        login_button = self.driver.find_element_by_css_selector(".button-login")
        login_button.click()
        self.check_layout("login page", "loginPage.spec", device.included_tags, device.excluded_tags)

