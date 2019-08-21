from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import bs4
import json

driver = webdriver.Firefox()
driver.get('http://www.organchem.csdb.cn/scdb/default.htm?nCount=12547440')

while '1' != input("登陆并切换到中药与化学成分数据库-中药复方检索页面后输入1"):
	pass

driver.switch_to.frame('main00')
searchInput = driver.find_element_by_name('RName')
searchInput.send_keys("安宫牛黄丸")
submitBtn = driver.find_element_by_name('submit1')
submitBtn.submit()
WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))

html = driver.page_source
soup = bs4.BeautifulSoup(html, 'html.parser')
result = []#盛放爬虫结果
if soup.find(class_='newform') is not None:
	result_list = soup.find(class_='newform').find_all('tr')[1:]#复方索引结果列表
else:
	print("无结果")
	exit(0)

Btns = driver.find_elements_by_name('FID')#复方索引结果对应“方剂描述”按钮


for i in range(len(Btns)):#遍历当前页面下的复方索引结果
	contents = result_list[i].find_all('td')#一个条目中的不同属性
	Btns = driver.find_elements_by_name('FID')#每次返回索引结果界面需要重新选中按钮
	string1 = " " if contents[1].string=='\xa0' else contents[1].string
	string2 = " " if contents[2].string=='\xa0' else contents[2].string
	string3 = " " if contents[3].string=='\xa0' else contents[3].string
	string4 = " " if contents[4].string=='\xa0' else contents[4].string
	string5 = " " if contents[5].string=='\xa0' else contents[5].string
	Btns[i].click()#点击条目对应“方剂描述”按钮
	WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('title_project2'))
	description = {}#盛放方剂描述
	description_title = driver.find_elements_by_class_name('title_project2')#方剂描述项标题
	description_content = driver.find_elements_by_class_name('content_project1')#方剂描述项内容
	for j in range(len(description_title)-1):#“治疗疾病”项单独处理
		description[description_title[j].text] = description_content[j].text
	if len(driver.find_elements_by_class_name('newform'))==0:
		description['治疗疾病'] = " "
	else:
		description['治疗疾病']=[]
		illness_list = driver.find_element_by_class_name('newform').find_elements_by_tag_name('tr')[1:]
		for illness in illness_list:#治疗疾病列表
			description['治疗疾病'].append({'主治疾病（西医病名）':illness.find_elements_by_tag_name('td')[1].text, '中医病名':illness.find_elements_by_tag_name('td')[2].text, '适宜证候':illness.find_elements_by_tag_name('td')[3].text, '适宜症状':illness.find_elements_by_tag_name('td')[4].text, '适宜体症':illness.find_elements_by_tag_name('td')[5].text})
	
	result.append({'方剂名称':string1, '服药方法':string2, '剂型':string3, '方型':string4, '主治证候':string5, '方剂描述':description})
	driver.back()
	WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name('newform'))
	
fout = open("result.json", "w", encoding='utf-8-sig')
json.dump(result, fout, ensure_ascii=False, indent=4, separators=(',', ': '))
print(result)
	