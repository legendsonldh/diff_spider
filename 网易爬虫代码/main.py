#-*-coding:utf-8-*-

from selenium import webdriver
import requests
import re
import os
from bs4 import BeautifulSoup
import time

os.makedirs('./meizi/ ' , exist_ok=False)

urls = ["http://jandan.net/ooxx/page-{}#comments".format(str(i)) for i in range(1, 48)]
# 定位Phantom.js 的参数设置
service_args=[]
# service_args.append('--load-images=no')  ##关闭图片加载
service_args.append('--disk-cache=yes')  ##开启缓存
service_args.append('--ignore-ssl-errors=true') ##忽略https错误
service_args.append('--ssl-protocol=any')##防止网站无法解析
d = webdriver.PhantomJS(service_args=service_args)

for url in urls:
    d.get(url)
    time.sleep(2)
    print(d.current_url)                # 查看链接是否污染
    data = d.page_source
    soup = BeautifulSoup(data, "lxml")  #解析网页
    img1 = soup.find_all("div",{"class":"text"})
    for img in img1:
        if str('gif') in str(img):
            pass
        else:
            img_url = img.find("img",{"src": re.compile('.*?\.jpg')})['src']
            r = requests.get(img_url, stream=True)
            image_name = img_url.split('/')[-1]
            with open('./meizi/%s' % image_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)
                print('Saved %s' % image_name)