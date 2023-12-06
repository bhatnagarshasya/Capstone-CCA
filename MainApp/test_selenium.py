import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        # Use EdgeOptions to set capabilities
        edge_options = webdriver.EdgeOptions()

        # Add any additional options as needed
        # For example, you may need to specify the Edge browser binary location
        # edge_options.binary_location = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

        self.driver = webdriver.Edge(options=edge_options)

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get('http://localhost:8080/')
        element = EC.presence_of_element_located('navbarSupportedContent')

    def test_search_in_python_org_prediction(self):
        driver = self.driver
        driver.get('http://localhost:8080/prediction')
        element = EC.presence_of_element_located('navbarSupportedContent')

    def test_search_in_python_org_report(self):
        driver = self.driver
        driver.get('http://localhost:8080/report')
        element = EC.presence_of_element_located('navbarSupportedContent')


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

