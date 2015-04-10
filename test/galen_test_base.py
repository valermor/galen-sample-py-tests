import os
import unittest
from galenapi.galen_api import Galen
from galenapi.galen_report import TestReport, info_node, warn_node, error_node
from galenapi.galen_webdriver import GalenWebDriver

PROJECT_NAME = 'galen-sample-py-tests'

FIREFOX = {
    "browserName": "firefox",
    "version": "",
    "platform": "ANY"
}


class GalenTestBase(unittest.TestCase):

    def setUp(self):
        self.driver = GalenWebDriver("http://localhost:4444/wd/hub", desired_capabilities=FIREFOX)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def load(self, url, width, height):
        self.driver.get(url)
        self.driver.set_window_size(width, height)

    def check_layout(self, test_name, specs, included_tags, excluded_tags):
        try:
            check_layout_report = Galen().check_layout(self.driver, os.path.join(os.path.dirname(__file__) + "/"
                                                                                    + "specs/" + specs)
                                                          , included_tags, excluded_tags)

            TestReport(test_name)\
                .add_report_node(info_node("Running layout check for: " + test_name)
                                 .with_node(warn_node('this is just a prototype'))
                                 .with_node(error_node('to demonstrate reporting')))\
                .add_layout_report_node("check " + specs, check_layout_report).finalize()
            if check_layout_report.errors > 0:
                raise AssertionError(
                    "Incorrect layout: " + test_name + " - Number of errors " + str(check_layout_report.errors))

        except Exception as e:
            raise e
