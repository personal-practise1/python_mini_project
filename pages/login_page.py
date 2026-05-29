from selenium.webdriver.common.by import By

class LoginPage:
    USERNAME=(By.ID,'user-name')
    PASSWORD=(By.ID,'password')
    LOGIN=(By.ID,'login-button')

    def __init__(self,driver):
        self.driver=driver

    def login(self,user,pwd):
        self.driver.find_element(*self.USERNAME).send_keys(user)
        self.driver.find_element(*self.PASSWORD).send_keys(pwd)
        self.driver.find_element(*self.LOGIN).click()
