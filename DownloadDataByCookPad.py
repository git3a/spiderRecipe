# 2017年12月6日 00点51分
# 作者：橘子派_司磊
# 爬虫：抓好豆菜谱
# 目标网址：http://www.haodou.com/recipe/30/

from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import re

# C:\Code\Recipes\Data\HaoDou\490
# C:\Code\Recipes\Data\HaoDou\14059_1201100

# 30-490 为页面简单
# 14059-1201100 为复杂
# id = 29
id = 4945532

# error_number为抓取错误的页面
error_number = 0
download_number = 1
while(id <= 4945532):
	id = id + 1
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
		
		url = requests.get('http://www.cookpad.com/recipe/'+str(id)+'/', headers=headers)
		print("当前爬取的网址为：" + url.url)
		html_doc = url.text
		soup = BeautifulSoup(html_doc,"lxml")
		#print(soup.prettify())
		recipe_name = soup.find(id="recipe-title").h1.string
		recipe_name = recipe_name.strip()
		print("菜谱的名字为：" + recipe_name)
		
		#img_html = soup.find(id="main-photo").src.string
		img_html = soup.find(id="main-photo").img.get('src')
		
		print("获取图片为：" + img_html)

		file = open('C:\\Users\\sun hong\\Desktop\\GIT3\\testcode\\spider\\SpiderRecipes\\download\\' + recipe_name + '.jpg',"wb")
		req = urllib.request.Request(url=img_html, headers=headers) 
		try:
			image = urllib.request.urlopen(req, timeout=10)
			pic = image.read()
		except Exception as e:
			print(e)
			print(recipe_name + "下载失败：" + img_html)

		file.write(pic)
		print("图片下载成功")
		file.close()

		drop_html = re.compile(r'<[^>]+>',re.S)
		date_reg_exp = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}')# 去掉日期开头的步骤
		full_text = []

		recipe_text = soup.find_all('dd')
		#print(recipe_text)
		for text_str in recipe_text:
			
			text = drop_html.sub('',str(text_str.find_all('p')))
			if (date_reg_exp.search(text) != None):
				#print('matched')
				continue
			
			text = text.replace("[", "")
			text = text.replace("]", "")
			if text != '':
				print(text)
				full_text.append(text)
	
		# print(recipe_text)
		file = open('C:\\Users\\sun hong\\Desktop\\GIT3\\testcode\\spider\\SpiderRecipes\\download\\' + recipe_name + '.txt', 'w')
		file.writelines(str(full_text))
		file.close()
	except Exception as e:
		print(e)
		error_number = error_number + 1
	else:
		continue
		download_number += 1
		if (download_number > 10): break

print("抓取错误的页面数量为：" + str(error_number))
