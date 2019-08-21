import os
import json

#清洗因gbk编码导致的错误文件

for root, dirs, files in os.walk('D:\\workspace\\spider\\化学专业数据库-中药\\中药复方\\data'):
	for file in files:
		with open(('D:\\workspace\\spider\\化学专业数据库-中药\\中药复方\\data\\' + file), encoding='gb18030') as f:
			try:
				json.load(f)
			except json.decoder.JSONDecodeError:
				print("删除了" + f.name)
				f.close()
				os.remove(f.name)
			else:
				f.close()