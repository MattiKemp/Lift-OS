import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'/home/ubuntu/Downloads/chromedriver',service_log_path='/home/ubuntu/logs/selenium')
driver.get('https://www.google.com/')
