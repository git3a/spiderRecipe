
# 目标网址：http://www.cookpad.com/recipe/

from bs4 import BeautifulSoup
import requests
import os
import urllib.request
import re
import MySQLdb

id = 4945000

# error_number为抓取错误的页面
error_number = 0
download_number = 0
try:
	db = MySQLdb.connect("/opt/bitnami/mysql/tmp/mysql.sock", "root", "Tfzn3FgkWDU2", "haochidb",charset='utf8')
except:
	print ("Could not connect to MySQL server.")
	exit( 0 )

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
		
		#材料
		ingredient_name = ''
		ingredient_quantity = ''
		ingredients = soup.find(id = 'ingredients_list')
		for child in ingredients.children:
			if (str(child).find('ingredient_category') != -1):
				continue
			drop_html = re.compile(r'<[^>]+>',re.S)
			text = drop_html.sub('',str(child))
			text = text.strip()
			if text != '':
				#print (text.split())
				text = text.split()
				ingredient_name +=(text[0] + '\n')
				ingredient_quantity += (text[1] + '\n')

		drop_html = re.compile(r'<[^>]+>',re.S)
		date_reg_exp = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}')# 去掉日期开头的步骤
		setp_text = ''

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
				#print(text)
				text = text.strip()
				setp_text+=(text + '\n')
	
		cursor = db.cursor()
		try:
			sql = "insert into testmodel_recipe(recipe_name, img_html, ingredient_name, ingredient_quantity, setp_text) values('%s','%s','%s','%s','%s')" % (recipe_name, img_html, ingredient_name, ingredient_quantity, setp_text)
			cursor.execute(sql)
			db.commit()
			#print ('db')
		except: 
			db.rollback()
			print ('db error')
	except Exception as e:
		print(e)
		error_number = error_number + 1
	else:
		download_number += 1
		if (download_number > 100): break
cursor.close()
print("抓取错误的页面数量为：" + str(error_number))
