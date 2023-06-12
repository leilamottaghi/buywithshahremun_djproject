
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from dict_all_size_guide import dict_sizeguide
from setting import tl_price
from woocommerce import API
import json
import sqlite3
import requests
import time
proxy_host = 'localhost:55579'
PROXY_USERNAME = "x7992"
PROXY_PASSWORD = "tohid123456789"
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
options = Options()
options.binary_location='C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
# options.add_argument('headless')
# options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})



wcapi = API(
	url="https://shahremun.com",
	consumer_key="ck_d06f06ed78809ba78c288ee7e34bb6dd729f5cdd",
	consumer_secret="cs_008d6ac981f1441351cead04a4106a13fe6410e0",
	# consumer_key="ck_c3668f8f752fc1ba5c8b1f698720d5ffd19ad2af",
	# consumer_secret="cs_8aa592e0336b6ba2dbf6e704a4c05c7e6012d9ef",
    version="wc/v3",
    timeout= 160
)


conn_costdb = sqlite3.connect('../shipping_cost.db',check_same_thread=False)
c_cost = conn_costdb.cursor()
def create_tables_cost():
	c_cost.execute('''CREATE TABLE IF NOT EXISTS categori_sku
			 (id integer primary key, name text , slug text,id_categori integer ,cost integer)''')
# create_tables_cost()



conn_dictdb = sqlite3.connect('../turk.db')
# conn.text_factory = str
c_dict = conn_dictdb.cursor()
def create_tables_dict():
	c_dict.execute('''CREATE TABLE IF NOT EXISTS color
			 (id integer primary key, tr text UNIQUE, fa text ,brandname_dict text)''')
	c_dict.execute('''CREATE TABLE IF NOT EXISTS material
			 (id integer primary key, tr text UNIQUE, fa text,brandname_dict text)''')
	c_dict.execute('''CREATE TABLE IF NOT EXISTS care
			 (id integer primary key, tr text UNIQUE, fa text,brandname_dict text)''')
	c_dict.execute('''CREATE TABLE IF NOT EXISTS description
			 (id integer primary key, tr text UNIQUE, fa text,brandname_dict text)''')

create_tables_dict()




# conn = sqlite3.connect('stock.db')
# c = conn.cursor()	
# def create_tables():
# 	c.execute('''CREATE TABLE IF NOT EXISTS urls
# 			 (id integer primary key, url text UNIQUE, barcode text,title text, categorie_id int,gharanti text,done int,tag_name text,tag_slug text,tag_id int)''')
# 	c.execute('''CREATE TABLE IF NOT EXISTS prev_stock
# 			 (id integer primary key, barcode text UNIQUE, price int, wp_id int, qty int, in_stock int)''')
# 	c.execute('''CREATE TABLE IF NOT EXISTS pre_process
# 			 (id integer primary key, barcode text, size text, price int,sales_price int, done int, title text, url text,image_list text, product_color text, country text,description text,gharanti text,supplier text,categorie_id text,image_name text,image_alt text,slug text,tag_name text,tag_slug text,tag_id int)''')
# 	c.execute('''CREATE TABLE IF NOT EXISTS product_sku
# 			 (id integer primary key, wp_sku text UNIQUE, wp_id integer, variation_id integer)''')






########################################crawl with beautifulsoup########################################


# def get_size(soup):
# 	try:
# 		time.sleep(3)
# 		first_div_sizes = soup.find("div", { "class" : "sizes-list-detail" })
# 		print("size div >>>>",first_div_sizes)
# 		if first_div_sizes:
# 			print("----have size-----")
# 			try:
# 				size_list = []
# 				size_list_div = first_div_sizes.find("ul", { "class" : "ui--size-dot-list" }).select('button.ui--dot-item.is-dot.is-naked:not(.ui--dot-item.is-dot.is-disabled.is-naked)')
# 				for size_div in size_list_div:
# 					span_size = size_div.select_one('span.text').get_text()
# 					print(span_size)
# 					size_list.append(span_size)
# 				return size_list
# 			except:
# 				print("hhh")
# 				time.sleep(3)
# 				try:
# 					last_text_is_disabled = soup.select_one('span.last-text.is-disabled')
# 					print("last_text_is_disabled =====>>>>",last_text_is_disabled)
# 					if last_text_is_disabled:
# 						return None
# 				except:
# 					button_is_black = soup.select_one('button.button.is-black:not(.button.is-black.is-disabled)')
# 					print("button_is_black =====>>>>",button_is_black)
# 					if button_is_black:
# 						return ["تک سایز"]
# 					else:
# 						return None
# 	except Exception as e:
# 		print(e)
# 		return None









# import requests 
# from requests_html import HTMLSession
# from bs4 import BeautifulSoup
# headers = {"User-Agent": "aUserAgent"}
# headers = {
#     'User-Agent': 'My User Agent 1.0',
#     'From': 'youremail@domain.example'  # This is another valid field
# }
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}




# def make_ready_breshka(url):
# 	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# 	# browser.get(url)
# 	session = HTMLSession()
# 	page = session.get(url)
# 	page.html.render()
# 	# page = requests.get(url, "html.parser",headers=headers)
# 	soup = BeautifulSoup(page.content, "html.parser")
# 	print(page.content)					
# 	size = get_size(soup)
# 	size_string = "|".join(size)
# 	print(size_string)
# 	# if size:
# 	# 	size_string = "|".join(size)
# 	# 	# categorie_id = int(200000)	
# 	# 	# price,sales_price = get_price(soup,categorie_id)
# 	# 	# print("price,sales_price ---->>>",price,sales_price)
# 	return size_string 
# 	# return size_string ,price,sales_price
	




# def make_ready_breshka(url):
# 	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# 	# browser.get(url)

# 	page = requests.get(url, "html.parser",headers=headers)
# 	soup = BeautifulSoup(page.content, "html.parser")
# 	print(page.content)					
# 	size = get_size(soup)
# 	size_string = "|".join(size)
# 	print(size_string)
# 	# if size:
# 	# 	size_string = "|".join(size)
# 	# 	# categorie_id = int(200000)	
# 	# 	# price,sales_price = get_price(soup,categorie_id)
# 	# 	# print("price,sales_price ---->>>",price,sales_price)
# 	return size_string 
# 	# return size_string ,price,sales_price
	
	


# --------------------------------------------crawl with selenium-------------------------------------------------------------
# def get_size(browser):
# 	try:
# 		time.sleep(3)
# 		first_div_sizes = browser.find_element(By.CLASS_NAME, 'sizes-list-detail')
# 		if first_div_sizes:
# 			print("----have size-----")
# 			try:
# 				size_list = []
# 				size_list_div = first_div_sizes.find_element(By.CLASS_NAME, 'ui--size-dot-list').find_elements(By.CSS_SELECTOR, 'button.ui--dot-item.is-dot.is-naked:not(.ui--dot-item.is-dot.is-disabled.is-naked)')
# 				for size_div in size_list_div:
# 					span_size = size_div.find_element(By.CSS_SELECTOR, 'span.text').text
# 					print(span_size)
# 					size_list.append(span_size)
# 				return size_list
# 			except:
# 				print("hhh")
# 				time.sleep(3)
# 				try:
# 					last_text_is_disabled = browser.find_element(By.CSS_SELECTOR, 'span.last-text.is-disabled')
# 					print("last_text_is_disabled =====>>>>",last_text_is_disabled)
# 					if last_text_is_disabled:
# 						return None
# 				except:
# 					button_is_black = browser.find_element(By.CSS_SELECTOR, 'button.button.is-black:not(.button.is-black.is-disabled)')
# 					print("button_is_black =====>>>>",button_is_black)
# 					if button_is_black:
# 						return ["تک سایز"]
# 					else:
# 						return None
# 	except Exception as e:
# 		print(e)
# 		return None






# def make_ready_bershka(url,browser):
# 	browser.get(url)
# 	try:
# 		time.sleep(2)
# 		cooki=browser.find_element(By.ID, "onetrust-accept-btn-handler")
# 		cooki.click()	
# 		time.sleep(5)								
# 		size = get_size(browser)
# 		if size:
# 			size_string = "|".join(size)
# 			# categorie_id = int(200000)	
# 			# price,sales_price = get_price(browser,categorie_id)
# 			# print("price,sales_price ---->>>",price,sales_price)

# 			# return size_string ,price,sales_price
		
# 			return size_string

		
# 	except Exception as e:

# 		# browser.refresh()
# 		time.sleep(5)								
# 		size = get_size(browser)
# 		if size:
# 			size_string = "|".join(size)
# 			# categorie_id = int(200000)	
# 			# price,sales_price = get_price(browser,categorie_id)
# 			# print("price,sales_price ---->>>",price,sales_price)

# 			# return size_string ,price,sales_price
		
# 			return size_string




def get_size(browser):
	try:
		# time.sleep(1)
		# wait = WebDriverWait(browser, 2)
		# first_div_sizes = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sizes-list-detail')))
		# first_div_sizes = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "sizes-list-detail")))
		browser.implicitly_wait(3)
		first_div_sizes = browser.find_element(By.CLASS_NAME, 'sizes-list-detail')
		if first_div_sizes:
			print("----have size-----")
			try:
				size_list = []
				size_list_div = first_div_sizes.find_element(By.CLASS_NAME, 'ui--size-dot-list').find_elements(By.CSS_SELECTOR, 'button.ui--dot-item.is-dot.is-naked:not(.ui--dot-item.is-dot.is-disabled.is-naked)')
				for size_div in size_list_div:
					span_size = size_div.find_element(By.CSS_SELECTOR, 'span.text').text
					print(span_size)
					size_list.append(span_size)
				return size_list
			except:
				print("hhh")
				time.sleep(3)
				try:
					last_text_is_disabled = browser.find_element(By.CSS_SELECTOR, 'span.last-text.is-disabled')
					print("last_text_is_disabled =====>>>>",last_text_is_disabled)
					if last_text_is_disabled:
						return None
				except:
					button_is_black = browser.find_element(By.CSS_SELECTOR, 'button.button.is-black:not(.button.is-black.is-disabled)')
					print("button_is_black =====>>>>",button_is_black)
					if button_is_black:
						return ["تک سایز"]
					else:
						return None
	except Exception as e:
		print(e)
		return []






def make_ready_bershka(url,browser):
	browser.get(url)
	# print("ddd",browser.page_source)	
	try:
		time.sleep(2)
		cooki=browser.find_element(By.ID, "onetrust-accept-btn-handler")
		cooki.click()
		time.sleep(4)	
		# print("ddd",browser.page_source)							
		size = get_size(browser)
		if size:
			size_string = "|".join(size)
			# categorie_id = int(200000)	
			# price,sales_price = get_price(browser,categorie_id)
			# print("price,sales_price ---->>>",price,sales_price)

			# return size_string ,price,sales_price

			status = "instock"
			return size_string ,status
		else:
			status = "outofstock"
			return size,status
		

		browser.quit()
	except Exception as e:
		size = get_size(browser)
		if size:
			size_string = "|".join(size)
			# categorie_id = int(200000)	
			# price,sales_price = get_price(browser,categorie_id)
			# print("price,sales_price ---->>>",price,sales_price)

			# return size_string ,price,sales_price
		

			status = "instock"
			return size_string ,status
		else:
			status = "outofstock"
			return size,status

		browser.quit()














# browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='104.0.5112.20').install()), options=options)
# url = "https://shop.mango.com/tr/erkek/pantolon-slim-fit/dar-kesim-renkli-jean-pantolon_37010801.html"
# make_ready_mango(url,browser)









