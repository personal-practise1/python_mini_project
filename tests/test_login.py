from pages.login_page import LoginPage
from utilities.read_config import ReadConfig
import time

class TestLogin:
    def test_valid_login(self, setup):
        driver = setup
        driver.get(ReadConfig.URL)
        LoginPage(driver).login(ReadConfig.USERNAME, ReadConfig.PASSWORD)
        assert "inventory" in driver.current_url
