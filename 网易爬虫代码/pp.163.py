#encoding=utf-8

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys 键盘按键导入
import requests
from bs4 import BeautifulSoup
import time
#import re 正则表达式
import os
import random

# 谷歌翻译模块，为我们建立目录做准备
from googletrans import Translator
translator = Translator(service_urls=[
      'translate.google.cn',
    ])
# img_title = translator.translate(img['title']).text
# 请求头
headers = {
    'Connection': 'close',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

# 页码寻找重启函数
def Page_Reset():
    page_num = 'page_num.txt'
    with open(page_num, 'w') as f:
        f.write("1")
        f.close()

# 使用Phantom.js 读取信息函数
def Get_url(url):
    try:
        d.get(url)
    except:
        print('please wait 120 seconds')
        # d.quit()
        time.sleep(120)
        d.get(url)
        print('Connection Rest')
    time.sleep(1)
    sp = BeautifulSoup(d.page_source, "html5lib")  # html5解析网页
    d.get('about:blank')
    return sp                                      # 返回解析过后的网址源码

# 建立一个目录
def Create_list(filename,name):
    if os.path.exists(filename) is True:
        print("%s finder have been existed" % name)
    else:
        os.mkdir(filename)
        print("%s finder have been created" % name)
    return

# 点赞数建立复杂目录
def Create_love(base):
    lis =[100,200,500,800,1000]
    # 只有人像进行了分类，其他的至少是喜欢数>200以上的
    for i in range(len(lis) - 1):
        what = '%s-%s' % (lis[i], lis[i + 1])
        Love = base + '/' + what
        Create_list(Love, what)
    return

# 将页码信息写入，以用重复查阅
def write_sth(txt,sth):
    with open(txt, 'w') as f:
        f.write("%s" % sth)
        f.close()

# 将页码信息读取
def read_sth(txt):
    if os.path.exists(txt) is True:
        with open(txt) as f:  # 默认模式为‘r’，只读模式
            content = int(f.read())  # 读取文件全部内容
            return content
    else:
        return 0

# 获取与下载

def Get_Download(url_cater,base_path):
    # 得到网址源码，开始获取信息
    sp = Get_url(url_cater)

    # 首先遍历所有页码数
    page_all = int(sp.find("span", {"class": "pgi zpg9 iblock"}).text) + 1

    # 读取已下载到的页码
    page_num = 'page_num.txt'
    contents = read_sth(page_num)

    contents = contents + 1 if (contents == 0) else contents

    for page in range(contents, page_all):
        end = time.clock()
        print('程序已运行:%s'%end)
        print('目前的目录是:%s'%t[i])
        if 'cid' in str(l[i]):
            print('子目录为：%s' %child.text)

        print('This is page:%s'%page)

        # 将页码信息写入，以用重复查阅
        write_sth(page_num,page)

        if page == 1:
            print('begin from 1')
            #pass
        else:
            img_page = url_cater.replace("page=1", "page=%s" % page)
            print(img_page)
            # 开始读取不同Page的信息
            sp = Get_url(img_page)

        # 每个小图组内含信息
        sp_group = sp.find_all('div', {"class": "detail f-trans"})
        for group in sp_group:

            # 网址信息

            img_url = group.find('a', {"class": "name js-name etag"})['href']   # 图组的网址
            Phrog_url = group.find('a', {"class": "js-uname uname etag"})['href'] # 摄影师主页

            # 名字信息，并进行一些防处理：去除'/',缩短我们所用的长度

            Couimg_name = group.find('a', {"class": "name js-name etag"}).text.replace('/','_')    # 图组的名字
            Phrog_name = group.find('a', {"class": "js-uname uname etag"}).text.replace('/','_')   # 摄影师名字

            finder_name = '%s_%s' % (Couimg_name[0:12], Phrog_name[0:2])      # 文件夹名字

            # 根据喜欢数建立文件夹；并下载

            # 这里会遇到空字符串的问题
            love_label = group.find('span', {"class": "js-like likeicn etag"}).text
            if love_label == '':
                love_num = 0
            else:
                love_num = int(love_label)

            # 建立文件夹
            img_path_finder = base_path + '/' + finder_name

            if 'cid' in str(l[i]):
                if 100 <= love_num < 200:
                    img_path_finder = base_path + '/100-200/' + finder_name
                elif 200 <=love_num < 500:
                    img_path_finder = base_path + '/200-500/' + finder_name
                elif 500 <= love_num < 800:
                    img_path_finder = base_path + '/500-800/' + finder_name
                elif 800 <= love_num :
                    img_path_finder = base_path + '/800-1000/' + finder_name
                elif love_num < 100:
                    continue
            else:
                if love_num >= 500:
                    img_path_finder = base_path + '/' + finder_name
                else:
                    continue


            # 检查文件夹是否存在，如果存在，则换下一个
            if os.path.exists(img_path_finder) is True:
                print("%s finder have been existed" % finder_name)
            else:
                os.mkdir(img_path_finder)
                print("%s finder have been created" % finder_name)
                print(img_path_finder)

                # 将摄影师相关信息写入，以便后期查看摄影师主页
                Pho = img_path_finder+'/'+'Pho.txt'
                with open(Pho, 'w') as f:
                    f.write("%s" % Phrog_url)
                    f.close()

                # 进入图组
                try:
                    s = BeautifulSoup(requests.get(img_url,headers=headers).text, 'html5lib')
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 120 seconds')
                    time.sleep(120)
                    s = BeautifulSoup(requests.get(img_url, headers=headers).text, 'html5lib')
                    print('Connection Rest')
                time.sleep(random.uniform(0.05,0.1))

                # 找到图库的所有图片

                img_pic = s.find_all('div', {"class": "pic-area"})

                for pic in img_pic:
                    imgs = pic.find_all('img')
                    for img_image in imgs:
                        url = img_image['data-lazyload-src']
                        try:
                            r = requests.get(url, stream=True,headers=headers)
                        except requests.exceptions.ConnectionError:
                            print('ConnectionError -- please wait 120 seconds')
                            time.sleep(120)
                            r = requests.get(url, stream=True, headers=headers)
                            print('Connection Rest')
                        time.sleep(random.uniform(0.05,0.1))

                        # 图片文件命名
                        image_name = url.split('/')[-1]
                        # 图片文件路径
                        img_path = img_path_finder + '/%s' %image_name
                        # 图片文件下载
                        if os.path.exists(img_path) == True:
                            print("pass")
                            #pass
                        else:
                            with open(img_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=128):
                                    f.write(chunk)

                    #if pic == img_pic[0]:
                        # print('Saved %s the first image' % image_name)
                # print('Saved %s the end image' % image_name)
    # 恢复初始页码
    Page_Reset()
    print('End with %s'%page_all)
    return

# 定位Phantom.js 的参数设置
service_args=[]
#service_args.append('--load-images=no')        ## 关闭图片加载
service_args.append('--disk-cache=yes')         ## 开启缓存
service_args.append('--ignore-ssl-errors=true') ## 忽略https错误
service_args.append('--ssl-protocol=any')       ## 防止网站无法解析
# 初始化PhantomJS
d = webdriver.PhantomJS(service_args=service_args)

# 程序开始计时
start = time.clock()

# 首先来到人像页面
url = 'http://pp.163.com/pp/#p=10&c=-1&m=3&page=1'
html = requests.get(url).text
sp = BeautifulSoup(html,'html5lib')

# 找到二级分类
l = sp.find('ul',{"class": "m-setnav"}).find_all('a')
# 初始化字典
u = []
t = []
del l[0],l[-2],l[-1]      # 去除头尾的："全部"与"精选"

for o in l:
    # 大分类从这里获取
    u.append(o['sid'])
    t.append(o.text[0:4].strip('\n\t'))

# 读取存入的分类信息
cater_num = read_sth('num.txt')

# 主程序，也是最大的循环
for i in range(cater_num,len(u)):
    # 写入标签循环
    write_sth('num.txt',i)

    # 建立第0级目录
    Create_list('./Photo','Photo')

    # 建立第一级目录
    base = './Photo/%s' % t[i]

    Create_list(base,t[i])

    # 获得次级网址与目录
    if 'cid' in str(l[i]):
        childItem = l[i].find_all('em')

        # 读取存入的信息
        child_num = read_sth('child.txt')    # 第一次运行时不要运行这一行命令

        for j in range(child_num,len(childItem)):

            child = childItem[j]

            # 写入标签循环
            write_sth('child.txt', j)

            url_cater = url.replace('p=10', 'p=%s' % u[i])

            # 第二级目录构建
            Second_list = base +'/'+child.text

            Create_list(Second_list,child.text)
            # 第三级目录构建

            Create_love(Second_list)

            # 切换到最终的网址
            url_cater = url_cater.replace('c=-1','c=%s' %child['cid'])
            Get_Download(url_cater,Second_list)

    else:
        url_cater = url.replace('p=10', 'p=%s' % u[i])
        # 切换到最终的网址
        Get_Download(url_cater, base)
