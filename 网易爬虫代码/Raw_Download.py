#-*-coding:utf-8-*-
#encoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import requests
from bs4 import BeautifulSoup
import time
#import re
import os
import random

url = 'https://www.wesaturate.com/'

# 使用Chrome 加载url
c = webdriver.Chrome()
# 设置超时时间
c.set_page_load_timeout(60)
c.set_script_timeout(60)
# 等待加载完成

try:
    c.get(url)
except:
    print("加载页面太慢，停止加载，继续下一步操作")

# 模拟鼠标与键盘操作
c.find_element_by_link_text("Login").click()
time.sleep(5)

# 先登陆
c.find_element_by_id('email-input').clear()
c.find_element_by_id('password-input').clear()

# 账号密码
c.find_element_by_id('email-input').send_keys('937074603@qq.com')
c.find_element_by_id('password-input').send_keys('RIapherkAwwial5')

# 点击登陆按钮
c.find_element_by_class_name('common-button-flat-purple').click()
time.sleep(4)

# 输入要搜索的图片
c.find_element_by_tag_name('input').send_keys('%s'%input())
"""
portrait    # 人像
"""

# 按下回车
c.find_element_by_tag_name('input').send_keys(Keys.RETURN)
time.sleep(2)

# BeautifulSoup 解析网页
sp = BeautifulSoup(c.page_source, "html5lib")  # html5解析网页

photo_url = sp.find_all("a",{"download":"download"})

img_path = '/Users/ludegao/Downloads/'


# 同时下载三个文件

for photo in photo_url:
    if photo.text == 'RAW':
        image_url = photo['href']
        image_name = image_url.split('/')[-1]
        image_path = img_path + image_name
        if os.path.exists(image_path) == True:
            pass
        else:
            c.get(image_url)
            time.sleep(60)

            while(os.path.exists(image_path+'.crdownload') == True):
                pass

            time.sleep(60)

            while(os.path.exists(image_path+'.crdownload') == True):
                break


