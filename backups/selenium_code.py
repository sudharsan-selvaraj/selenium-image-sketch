from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options, executable_path ="/Users/sudharsan/Documents/Applications/chromedriver")
driver.get("https://vrobbi-nodedrawing.herokuapp.com/")
body_element = driver.find_element_by_tag_name("body")

sleep(2)
actions = ActionChains(driver)
actions.move_to_element_with_offset(body_element, 100, 100)\
    .click_and_hold()\
    .move_to_element_with_offset(body_element, 120, 100)\
    .release().perform()
sleep(20)



