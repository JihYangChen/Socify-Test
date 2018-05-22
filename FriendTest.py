import unittest
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os


class FriendTest(unittest.TestCase):

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

    def test_01_follow_friend(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='links']/h5[6]/a").click()

        driver.find_element_by_xpath("//*[@id='user-1']/div[2]/div/div/form/button").click()
        time.sleep(1)
        followButton = driver.find_element_by_xpath("//*[@id='user-1']/div[2]/div/div/form/button")

        self.assertEqual("unfollow", followButton.text)

    def test_02_unfollow_friend(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='links']/h5[4]/a").click()

        driver.find_element_by_xpath("//*[@id='user-1']/div[2]/div/div/form/button").click()
        time.sleep(1)
        followButton = driver.find_element_by_xpath("//*[@id='user-1']/div[2]/div/div/form/button")

        self.assertEqual("follow", followButton.text)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()