import unittest
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os


class StatusTest(unittest.TestCase):

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

    def test_01_create_new_status(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='post-content']").send_keys("Hello World!")
        driver.find_element_by_xpath("//*[@id='new_post']/div[4]/input").submit()

        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        postAction = latestPostDiv.find_element_by_xpath("//span[@class='action']").text
        postUserName = latestPostDiv.find_element_by_xpath("//h4[@class='name']/a").text
        postUserContent = latestPostDiv.find_element_by_xpath("//div[@class='content']//p").text

        self.assertEqual("created a post", postAction)
        self.assertEqual(self.userName, postUserName)
        self.assertEqual("Hello World!", postUserContent)

    def test_02_create_new_status_with_no_content(self):
        driver = self.driver
        driver.find_element_by_xpath("//*[@id='new_post']/div[4]/input").submit()
        errorMessage = driver.find_element_by_xpath("/html/body/div[1]").text.rstrip('\n×')
        self.assertEqual("Content can't be blank", errorMessage)

    def test_03_create_new_status_with_image(self):
        driver = self.driver

        driver.find_element_by_xpath("//*[@id='post-content']").send_keys("Hello World!")
        driver.find_element_by_xpath("//input[@type='file']").send_keys(os.getcwd()+"\hello.jpg")
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='new_post']/div[4]/input").submit()

        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        postAction = latestPostDiv.find_element_by_xpath("//span[@class='action']").text
        postUserName = latestPostDiv.find_element_by_xpath("//h4[@class='name']/a").text
        postUserContent = latestPostDiv.find_element_by_xpath("//div[@class='content']//p").text

        self.assertEqual("created a post", postAction)
        self.assertEqual(self.userName, postUserName)
        self.assertEqual("Hello World!", postUserContent)

        deleteButton = latestPostDiv.find_element_by_xpath("//a[@class='btn btn-danger btn-sm']")
        deleteButton.click()

    def test_04_edit_status(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        editButton = latestPostDiv.find_element_by_xpath("//a[@class='btn btn-primary btn-sm']")
        editButton.click()

        driver.find_element_by_xpath("//*[@id='post-content']").send_keys("Ya! ")
        driver.find_element_by_xpath("//*[@id='post_content']").submit()

        postUserContent = driver.find_element_by_xpath("//div[@class='content']//p").text

        self.assertEqual("Ya! Hello World!", postUserContent)

    def test_05_comment_post(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        commentButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 comment']//a")
        commentButton.click()

        driver.find_element_by_xpath("//*[@id='comment-text']").send_keys("Good!")
        driver.find_element_by_xpath("//*[@id='comment-text']").submit()

        time.sleep(1)
        commentContent = driver.find_element_by_xpath("//div[2]/div[1]/span/p").text

        self.assertEqual("Good!", commentContent)

    def test_06_delete_comment(self):
        driver = self.driver
        # goto comment page
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        commentButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 comment']//a")
        commentButton.click()

        # delete comment
        deleteButton = driver.find_element_by_xpath("//*/div[2]/div[2]/a")
        deleteButton.click()
        time.sleep(1)

        with self.assertRaises(NoSuchElementException):
            driver.find_element_by_xpath("//*/div[2]/div[2]/a")

    def test_07_like_post(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        likeButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 like']//button")
        likeButton.click()
        time.sleep(1)

        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][2]".format(self.userName))
        likeButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 like']//button")

        self.assertEqual("unlike", likeButton.text)

    def test_08_unlike_post(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][2]".format(self.userName))
        likeButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 like']//button")
        likeButton.click()
        time.sleep(1)

        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][2]".format(self.userName))
        likeButton = latestPostDiv.find_element_by_xpath("//div[@class='col-xs-6 like']//button")

        self.assertEqual("like", likeButton.text)

    def test_09_delete_status(self):
        driver = self.driver
        latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
        deleteButton = latestPostDiv.find_element_by_xpath("//a[@class='btn btn-danger btn-sm']")
        deleteButton.click()
        time.sleep(1)

        with self.assertRaises(NoSuchElementException):
            latestPostDiv = driver.find_element_by_xpath("//div[@class='activity' and .//h4[@class='name']/a[text()='{0}']][1]".format(self.userName))
            latestPostDiv.find_element_by_xpath("//div[@class='content']//p[text()='Hello World!']")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()