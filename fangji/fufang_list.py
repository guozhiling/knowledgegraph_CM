from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from login import random_login
#from random_ip import __get_random_ip
#from headers_list import headers_list
from abu_ip import abu_ip
import random


def get_fangji_rows(driver, list, num):
	fangji_results = driver.find_element_by_class_name('newform').find_elements_by_tag_name('tr')[1:]
	for fangji_result in fangji_results:
		list.append(fangji_result.find_elements_by_tag_name('td')[1].text)
		num = num+1
		if num%100 == 0:
			print("第"+str(num)+"个药方")
			print(list[len(list)-1])
	return num

def get_illness_rows(driver, list, num, operates):
	Btns = driver.find_elements_by_name('FID')
	for i in range(len(Btns)):
		driver.find_elements_by_name('FID')[i].click()
		print("点击当前页面第" + str(i+1) + "种病名")
		WebDriverWait(driver,10).until(lambda x: x.find_element_by_name('Dis_pres_id'))
		driver.find_element_by_name('Dis_pres_id').click()
		WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))
		operates = operates + 2
		if driver.find_elements_by_class_name('newform')==[]:
			break

		next_times = 0#用来记录下一页的次数
		while driver.find_elements_by_name('next'):
			#print(driver.find_elements_by_name('next')[0].text)
			num = get_fangji_rows(driver, fangji_list, num)
			driver.find_element_by_name('next').click()
			WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))
			next_times = next_times + 1
		num = get_fangji_rows(driver, fangji_list, num)
		for j in range(next_times+2):
			driver.back()
		operates = operates + next_times*2
	return num, operates


#driver = webdriver.Firefox()
#driver.get('http://www.organchem.csdb.cn/scdb/default.htm?nCount=12547440')
#driver.add_cookie(cookie_dict={'name':'ASPSESSIONIDSQCQRTSR', 'value':'ENPNCKJADNAIICEJEMOOFFHL'})

num = 0#记录药方数
operates = 0#记录切换页面次数，避免封号
status = 1#记录爬虫是否需要中断，0为中断
fangji_list = []
option = webdriver.FirefoxOptions()

for i in range(1, 35):
	#ip = __get_random_ip()
	#header = headers_list[random.randint(0,5)]
	#argument_str = "--proxy-server=http://"+ip
	#option.add_argument('user-agent="' + header + '"')
	#option.add_argument(argument_str)
	#option.set_headless()
	#driver = webdriver.Firefox(options=option)
	#driver.delete_all_cookies()
	driver = abu_ip()
	random_login(driver)
	temp_fangji_list = []
	print("抓取第"+str(i)+"个科属")
	driver.get('http://www.organchem.csdb.cn/scdb/Tcm_Multi/q_disease.asp')
	WebDriverWait(driver,10).until(lambda x: x.find_element_by_name('disbranch'))
	S = Select(driver.find_element_by_name('disbranch')).select_by_index(i)
	submitBtn = driver.find_element_by_name('submit1')
	submitBtn.submit()
	WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))
	page = 0
	operates = 0

	if driver.find_elements_by_class_name('newform') is []:
		break
	while driver.find_elements_by_name('next'):
		num, operates = get_illness_rows(driver, temp_fangji_list, num, operates)
		page = page + 1
		if operates >= 50:
			print("已经进行了" + str(operates) + "次页面切换操作")
			input("按任意键继续")
			status = 0
			driver.close()
			#ip = __get_random_ip()
			#argument_str = "--proxy-server=http://"+ip
			#option.add_argument(argument_str)
			driver = abu_ip()
			driver.delete_all_cookies()
			random_login(driver)
			driver.get('http://www.organchem.csdb.cn/scdb/Tcm_Multi/q_disease.asp')
			WebDriverWait(driver,10).until(lambda x: x.find_element_by_name('disbranch'))
			S = Select(driver.find_element_by_name('disbranch')).select_by_index(i)
			submitBtn = driver.find_element_by_name('submit1')
			submitBtn.submit()
			WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))
			for k in range(page-1):
				driver.find_element_by_name('next').click()
				WebDriverWait(driver,10).until(lambda x: x.find_element_byclass_name('newform'))
			status = 1
			input("按任意键继续")
		driver.find_element_by_name('next').click()
		input("按任意键继续")
		WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))


	get_illness_rows(driver, temp_fangji_list, num, operates)
	temp_fangji_list = list(set(temp_fangji_list))
	tempfout = open("fangji"+str(i)+".list", "w", encoding='utf-8-sig')
	for temp_fangji in range(len(temp_fangji_list)):
		fout.write(temp_fangji + "\n")
	fangji_list.extend(temp_fangji_list)
	driver.close()

fangji_list = list(set(fangji_list))

fout = open("fangji.list", "w", encoding='utf-8-sig')
for fangji in range(len(fangji_list)):
	fout.write(fangji + "\n")