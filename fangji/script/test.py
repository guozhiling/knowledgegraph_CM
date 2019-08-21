from selenium import webdriver
from random_ip import __get_random_ip
from login import login_main


option = webdriver.FirefoxOptions()
ip = __get_random_ip()
argument_str = "--proxy-server=http://"+ip
option.add_argument(argument_str)
driver = webdriver.Firefox(options=option)

login_main(driver)
