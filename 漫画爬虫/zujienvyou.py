#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#encoding=utf-8

from selenium import webdriver    
import requests
from bs4 import BeautifulSoup
import time
import random
import os
import re
from requests.packages import urllib3
# 建立一个目录
def Create_list(filename,name):
    if os.path.exists(filename) is True:
        print("%s finder have been existed" % name)
    else:
        os.mkdir(filename)
        print("%s finder have been created" % name)
    return
# 将页码信息写入，以用重复查阅
def write_sth(txt,sth):
    with open(txt, 'w') as f:
        f.write("%s" % sth)
        f.close()

# 将页码信息读取
def read_sth(txt):
    if os.path.exists(txt) is True:
        with open(txt) as f:         # 默认模式为‘r’，只读模式
            content = int(f.read())  # 读取文件全部内容
            return content
    else:
        return 0                     # 因为列表的第一个元素的位置是[0]，所有返回0
# 不加载图片
def d_unimg():
    options = webdriver.ChromeOptions()    
    #加上下面两行，解决报错
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu') 
    options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    chromedriver = '/Users/ludegao/bin/chromedriver'
    d = webdriver.Chrome(chromedriver,options=options)
    return d
# 加载图片
def d_img():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #加上下面两行，解决报错
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu') 
    options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    #options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    chromedriver = '/Users/ludegao/bin/chromedriver'
    d = webdriver.Chrome(chromedriver,options=options)
    return d
# 读取网页信息
def Get_url(url):
    try:
        d.get(url)
    except:
        print('please wait 120 seconds')           # 如果出现异常，则等待120s，重启读取
        # d.quit()
        time.sleep(120)
        d.get(url)
        print('Connection Rest')
    time.sleep(1)
    sp = BeautifulSoup(d.page_source, "html5lib")  # html5解析网页
    d.get('about:blank')                           # 这个很关键，防止出现链接污染
    return sp                                      # 返回解析过后的网址源码

# 首先来到首页
url = 'https://www.mangabz.com/279bz'
d  = d_unimg()
sp = Get_url(url)
# 找到数字
l = sp.find('div',{"class": "detail-list-form-con"}).find_all('a')
# 放网址和title
u = []
n = []
t = []
for o in l:
    un = re.findall(r"\d+\.?\d*",o.text)
    if len(un) != 1:
        u.append(un[0])
        n.append(un[-1])
        t.append(o['href'])
    

# 进入下一级页面
# 0-101
for i in range(95,-1,-1):
    # 创建文件夹
    floder_path = './zujienvyou/'+u[i]+'/'
    page_num    = floder_path+'page_num.txt'
    # 创建文件夹
    os.makedirs(floder_path, exist_ok=True)
    # 检查文件夹
    if os.path.exists(floder_path) is True:
        print(u[i]+'已存在')
        if os.path.exists(page_num) is False:
            write_sth(page_num,1)
        # 如果全部下完？
        if read_sth(page_num) == int(n[i]):
            print(u[i]+'已下完')
        if read_sth(page_num) == 1:
            print(u[i]+'开始下载')
            # 首页和最后一页不要
            for j in range(1,int(n[i])+1):
                url = 'https://www.mangabz.com'+t[i]+'#ipg'+str(j)
                # 开启加载图片
                d = d_img()
                sp1 = Get_url(url)
                im = sp1.find('img',{"id": "cp_image"})
                img= im.get('src')
                # 下载
                try:
                    urllib3.disable_warnings()
                    r = requests.get(img, stream=True,verify=False)
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 60 seconds')
                    time.sleep(60)
                    urllib3.disable_warnings()
                    r = requests.get(img, stream=True,verify=False)
                    print('Connection Rest')   
                time.sleep(random.uniform(0.05,0.1))
                image_name = str(j)+'.jpg'
                Dl_path = floder_path+image_name
                with open(Dl_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=64):
                        f.write(chunk)                        
                write_sth(page_num,j)                
                print('Saved %s' % image_name)
    
        # 检查页数是否全部下完
        if read_sth(page_num) != 1 & read_sth(page_num) != int(n[i]):
            p_num = read_sth(page_num)  
            print('已下载'+str(p_num)+'页')
            # 断点开始下载
            for j in range(p_num+1,int(n[i])):
                url = 'https://www.mangabz.com'+t[i]+'#ipg'+str(j)
                # 开启加载图片
                d = d_img()
                sp1 = Get_url(url)
                im = sp1.find('img',{"id": "cp_image"})
                img= im.get('src')
                # 下载
                try:
                    urllib3.disable_warnings()
                    r = requests.get(img, stream=True,verify=False)
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 60 seconds')
                    time.sleep(60)
                    urllib3.disable_warnings()
                    r = requests.get(img, stream=True,verify=False)
                    print('Connection Rest')   
                time.sleep(random.uniform(0.05,0.1))
                image_name = str(j)+'.jpg'
                Dl_path = floder_path+image_name
                with open(Dl_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=64):
                        f.write(chunk)
                print('Saved %s' % image_name)
                write_sth(page_num,j)  


