
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time,datetime

profile = webdriver.FirefoxProfile()
driver = webdriver.Chrome(os.path.abspath("/Users/brandonpeck/Downloads/chromedriver"))
driver.get("http://localhost:8000/")
#assert "Welcome to AirClean" in driver.title
username = "useruser11"
password = "password"
#register
driver.find_element_by_xpath("""//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[2]/a""").click()
driver.find_element_by_xpath("""//*[@id="id_username"]""").send_keys(username)
driver.find_element_by_xpath("""//*[@id="id_password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@id="id_first_name"]""").send_keys("bobert")
driver.find_element_by_xpath("""//*[@id="id_last_name"]""").send_keys("bobert")
driver.find_element_by_xpath("""/html/body/div/form/input[2]""").click()

#login
driver.find_element_by_xpath("""//*[@id="id_username"]""").send_keys(username)
driver.find_element_by_xpath("""//*[@id="id_password"]""").send_keys(password)
driver.find_element_by_xpath("""/html/body/div/form/input[2]""").click()

#add job
job_name ="new job 1"
job_description ="description"
job_price = 5
job_loc ="Hartford, CT"
driver.find_element_by_xpath("""//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[2]/a""").click()
driver.find_element_by_xpath("""//*//*[@id="id_name"]""").send_keys(job_name)
driver.find_element_by_xpath("""//*[@id="id_description"]""").send_keys(job_description)
driver.find_element_by_xpath("""//*[@id="id_price"]""").send_keys(job_price)
driver.find_element_by_xpath("""//*[@id="id_location"]""").send_keys(job_loc)
driver.find_element_by_xpath("""/html/body/div/form/input[2]""").click()

#check job added in home
assert job_name in driver.page_source

#check job created page
driver.find_element_by_link_text("""new job 1""").click()
driver.find_element_by_xpath("""/html/body/div/div/a""").click()


#check search index
driver.find_element_by_xpath("""//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[2]/a""").click()
driver.find_element_by_xpath("""//*[@id="id_search"]""").send_keys(job_name)
driver.find_element_by_xpath("""/html/body/div/form/input[2]""").click()
assert job_name in driver.page_source


time.sleep(2)
driver.close()