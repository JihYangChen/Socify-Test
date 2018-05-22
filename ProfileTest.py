import unittest
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os


class ProfileTest(unittest.TestCase):

    def setUp(self):
        chrome_path = "C:\selenium_driver_chrome\chromedriver.exe"
        self.driver = webdriver.Chrome(chrome_path)
        self.socifyURL = "http://140.124.183.102:3000"
        self.userEmail = "t106598014@ntut.org.tw"
        self.userPassword = "106598014"
        self.userName = "Hmm?"

        self.login()

    def login(self):
        driver = self.driver
        driver.get(self.socifyURL)
        self.assertIn("Socify", driver.title)

        driver.find_element_by_xpath("//*[@id='navbar-top']/ul/li[3]/a").click()
        driver.find_element_by_xpath("//*[@id='user_email']").send_keys(self.userEmail)
        driver.find_element_by_xpath("//*[@id='user_password']").send_keys(self.userPassword)
        driver.find_element_by_xpath("//*[@id='user_password']").submit()
        assert "Log in" not in driver.page_source

    def test_01_edit_profile(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='links']/h5[7]/a").click()

        # edit profile fields
        driver.find_element_by_xpath("//input[@type='file' and @name='user[avatar]']").send_keys(os.getcwd() + "\hmm.jpg")
        driver.find_element_by_xpath("//input[@type='file' and @name='user[cover]']").send_keys(os.getcwd() + "\cover.jpg")
        driver.find_element_by_xpath("//*[@id='user_name']").clear()
        driver.find_element_by_xpath("//*[@id='user_name']").send_keys("Hmm?")
        driver.find_element_by_xpath("//*[@id='user_about']").clear()
        driver.find_element_by_xpath("//*[@id='user_about']").send_keys("About me")
        driver.find_element_by_xpath("//*[@id='user_location']").clear()
        driver.find_element_by_xpath("//*[@id='user_location']").send_keys("Taipei")
        driver.find_element_by_xpath("//*[@id='user_phone_number']").clear()
        driver.find_element_by_xpath("//*[@id='user_phone_number']").send_keys("0912456789")
        driver.find_element_by_xpath("//*[@id='user_dob']").clear()
        driver.find_element_by_xpath("//*[@id='user_dob']").send_keys("2018/05/17")
        driver.find_element_by_xpath("//*[@id='user_sex']/option[2]").click()

        driver.find_element_by_xpath("//div[9]/input").click()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()