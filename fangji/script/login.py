from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from login_dict import login_dict
import random


#	driver = webdriver.Firefox()#单独调试时用

def login_main(driver):

	driver.get('http://www.organchem.csdb.cn/scdb/default.htm?nCount=12547440')
	#driver.switch_to.frame('main00')#本意是等待网页加载，不知道为什么不起作用反而报错
	#WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('Username'))

	driver.switch_to.frame('main00')
	loginInput = driver.find_element_by_name('Username')
	loginInput.send_keys("轩辕虚玄")
	passwordInput = driver.find_element_by_name('Password')
	passwordInput.send_keys("VoidXyxx3103")
	submitBtn = driver.find_element_by_name('login')
	submitBtn.click()

def login(driver, index=0):
	driver.get('http://www.organchem.csdb.cn/scdb/default.htm?nCount=12547440')
	driver.switch_to.frame('main00')
	loginInput = driver.find_element_by_name('Username')
	loginInput.send_keys(login_dict[index]['Username'])
	passwordInput = driver.find_element_by_name('Password')
	passwordInput.send_keys(login_dict[index]['Password'])
	submitBtn = driver.find_element_by_name('login')
	submitBtn.click()

def random_login(driver):
	index = random.randint(0, 2)
	print("使用第" + str(index+1) + "个账号")
	login(driver, index)