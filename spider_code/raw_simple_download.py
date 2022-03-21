#-*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import requests
from bs4 import BeautifulSoup
import time
#import re
import os
import random

url = 'https://www.wesaturate.com/search/%s'%input()

# 使用Chrome 加载url
c = webdriver.Chrome()
# 设置超时时间
c.set_page_load_timeout(20)
c.set_script_timeout(20)
# 等待加载完成
html = requests.get(url).text
sp = BeautifulSoup(html, "html5lib")  # html5解析网页
photo_url = sp.find_all("a",{"download":"download"})

print(photo_url)

input()
c.get(url)

try:
    c.get(url)
except:
    print("加载页面太慢，停止加载，继续下一步操作")

# BeautifulSoup 解析网页
sp = BeautifulSoup(c.page_source, "html5lib")  # html5解析网页

photo_url = sp.find_all("a",{"download":"download"})

for photo in photo_url:
    if photo.text == 'RAW':
        c.get(photo['href'])