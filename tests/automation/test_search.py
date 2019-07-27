import os
import unittest
from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.support.select import Select


class PythonOrgSearch(TestCase):
    BASE_URL = os.environ.get('FRONTEND_ADDRESS', 'http://localhost:4200')

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_by_customer_name(self):
        self.driver.get(self.BASE_URL)
        self.assertNotIn('VLUR4X20009093588', self.driver.page_source)

        customer_name_element = self.driver.find_element_by_css_selector('.vehicle__search-field input')
        customer_name_element.send_keys('kalles')
        self.assertIn('VLUR4X20009093588', self.driver.page_source)

    def test_search_by_online_status(self):
        self.driver.get(self.BASE_URL)
        self.assertNotIn('VLUR4X20009093588', self.driver.page_source)

        select = self.driver.find_element_by_css_selector('.vehicle__select-field mat-select')
        select.click()
        offline = self.driver.find_element_by_css_selector('#mat-option-2')
        offline.click()

        self.assertIn('VLUR4X20009093588', self.driver.page_source)

    def test_search_by_online_status_and_customer_name(self):
        self.driver.get(self.BASE_URL)
        self.assertNotIn('VLUR4X20009093588', self.driver.page_source)

        customer_name_element = self.driver.find_element_by_css_selector('.vehicle__search-field input')
        customer_name_element.send_keys('kalles')
        select = self.driver.find_element_by_css_selector('.vehicle__select-field mat-select')
        select.click()
        offline = self.driver.find_element_by_css_selector('#mat-option-2')
        offline.click()

        self.assertIn('VLUR4X20009093588', self.driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
