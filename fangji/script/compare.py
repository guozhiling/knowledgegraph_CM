#对比文件目录与网页目录，达到总数24858
import os
import requests
import bs4
import re
import json

html = requests.get('http://zhongyaofangji.com/all.html')
html.encoding = 'gb18030'
html = html.text
soup = bs4.BeautifulSoup(html, 'html.parser')
r = re.compile(r'[【](.*?)[】]')

all_list = soup.find('ul', class_='uzyc').find_all('li')

for fangji in all_list:
	fangji_name = fangji.find('a').text
	fangji_name = fangji_name.replace('/', '-')
	if fangji_name == "嗳气吞酸":#第一个症状，之前全是方剂
		break
	if not os.path.isfile("./data/" + fangji_name + ".json"):
		print(fangji_name + "未收录")
		fangji_url = fangji.find('a').attrs['href']
		detail_html = requests.get(fangji_url, timeout=10)
		detail_html.encoding = 'gb18030'
		detail = detail_html.text
		detail_soup = bs4.BeautifulSoup(detail, 'html.parser')
		contentlist = detail_soup.find('div', class_='spider').find_all('p')
		data = {'方剂名称': fangji_name,
				'url': fangji_url,}
		temptitle = None#有一些描述没有标题，用于将这样的描述添加到上一描述
		for content in contentlist:
			#print(content.text)
			if re.match(r, content.text) is not None:
				title = re.match(r, content.text).group()
				description = re.sub(u"【.*?】", "", content.text)
				data[title] = description
				temptitle = title
			else:
				description = re.sub(u"【.*?】", "", content.text)
				data[temptitle] = data[temptitle] + "    " +description#同一描述的两行之间用4个空格分开
		tempfile = open("./data/" + fangji_name + ".json", "w", encoding='gb18030')
		json.dump(data, tempfile, ensure_ascii=False, indent=4, separators=(',', ': '))
		print(data)
		print(fangji_name + "已收录")
		tempfile.close()