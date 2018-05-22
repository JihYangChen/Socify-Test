import unittest
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


class EventTest(unittest.TestCase):

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

    def test_01_create_new_event(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='links']/h5[2]/a").click()
        driver.find_element_by_xpath("//*[@id='event_name']").send_keys("Test Event")
        driver.find_element_by_xpath("//*[@id='event_event_datetime']").send_keys("2018/05/20 18:14")
        driver.find_element_by_xpath("//*[@id='new_event']/div[3]/input").submit()

        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        postAction = latestPostDiv.find_element_by_xpath("//span[@class='action']").text
        postUserName = latestPostDiv.find_element_by_xpath("//h4[@class='name']/a").text
        eventName = latestPostDiv.find_element_by_xpath("//div[@class='content']/h3").text
        eventDate = latestPostDiv.find_element_by_xpath("//div[@class='content']/span").text.rstrip('\n×')

        self.assertEqual("created an event", postAction)
        self.assertEqual(self.userName, postUserName)
        self.assertEqual("Test Event", eventName)
        self.assertEqual("20 May 18:14", eventDate)

    def test_02_create_new_event_with_no_content(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='links']/h5[2]/a").click()
        driver.find_element_by_xpath("//*[@id='new_event']/div[3]/input").submit()

        assert "Update Status." not in driver.page_source

    def test_03_edit_event(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        editButton = latestPostDiv.find_element_by_xpath("//a[@class='btn btn-primary btn-sm']")
        editButton.click()

        # update event info
        driver.find_element_by_xpath("//*[@id='event_name']").clear()
        driver.find_element_by_xpath("//*[@id='event_name']").send_keys("Test New Event")
        driver.find_element_by_xpath("//*[@id='event_event_datetime']").clear()
        driver.find_element_by_xpath("//*[@id='event_event_datetime']").send_keys("2018/05/20 19:20")
        driver.find_element_by_xpath("//div[3]/input").submit()

        # locate new event info DOM
        postUserName = driver.find_element_by_xpath("//h4[@class='name']/a").text
        postAction = driver.find_element_by_xpath("//div[1]/div/div[1]/span").text
        eventName = driver.find_element_by_xpath("//div[@class='content']/h3").text
        eventDate = driver.find_element_by_xpath("//div[@class='content']/span").text.rstrip('\n×')

        self.assertEqual("created an event", postAction)
        self.assertEqual(self.userName, postUserName)
        self.assertEqual("Test New Event", eventName)
        self.assertEqual("20 May 19:20", eventDate)

    def test_04_delete_event(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        deleteButton = latestPostDiv.find_element_by_xpath("//a[@class='btn btn-danger btn-sm']")
        deleteButton.click()
        time.sleep(1)

        with self.assertRaises(NoSuchElementException):
            latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
            latestPostDiv.find_element_by_xpath(".//i[@class='fa fa-calendar']")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()