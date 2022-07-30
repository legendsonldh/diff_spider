# -*- coding: utf-8 -*-
"""
-----------------------------------------------------------------
Autor:    ludeh
Time:     2022-07-24
Version:  0.1
-----------------------------------------------------------------
    
This script need these lib
    
    pip install bs4       ----- change webpage to struct
    pip install html5lib  ----- help bs4
    pip install Selenium  ----- webdriver simulate 
    pip install requests  ----- strong web 
    pip install re        ----- extract things we need
    pip install tqdm      ----- progress
    pip install pyautogui ----- simulate the input of keyboard
    pip install pyperclip ----- clipboard
    pip install PIL       ----- Image lib
    
-----------------------------------------------------------------
"""
import requests
import time
import random
import os
import re
import pyautogui
import pyperclip
from enum import Enum
from PIL import Image
from io import BytesIO
from requests.packages import urllib3
from selenium import webdriver    
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from tqdm import tqdm

global BrowserType

BrowserType = 1 # 1:Chrome

class BrowserTypeFlag(Enum):
    Chrome  = 1
    Firefox = 2


# create a content
def createFolder(filename,name):
    if os.path.exists(filename) is True:
        print("%s finder have been existed" % name)
    else:
        os.mkdir(filename)
        print("%s finder have been created" % name)
    return

# write the pageflag
def writePageFlag(txt,sth):
    with open(txt, 'w') as f:
        f.write("%s" % sth)
        f.close()

# read the pageflag
def readPageFlag(txt):
    if os.path.exists(txt) is True:
        with open(txt) as f:         # 默认模式为‘r’，只读模式
            content = int(f.read())  # read all content 
            return content
    else:
        return 0                     # 因为列表的第一个元素的位置是[0]，所有返回0




"""
we have too mode and one will load image
Important: 
    (Windows) you should add the webdriver into the system path
    (Macos) you should change funtion webdriver.Firefox(...)
"""
# no load image mode
def noImageModeBrowser():  
    if BrowserType == BrowserTypeFlag.Chrome.value:
        options = webdriver.ChromeOptions()  
    else:
        options = webdriver.FirefoxOptions() 

    #加上下面两行，解决报错
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu') 
    options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
    
    if BrowserType == BrowserTypeFlag.Chrome.value:
        noImageBrowser = webdriver.Chrome(options=options)  
    else:
        noImageBrowser = webdriver.Firefox(options=options)      
    
    return noImageBrowser

# load image mode
def ImageModeBrowser():
    if BrowserType == BrowserTypeFlag.Chrome.value:
        options = webdriver.ChromeOptions()  
    else:
        options = webdriver.FirefoxOptions() 
        
    #options.add_argument('--headless')
    
    #加上下面两行，解决报错
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu') 
    options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面

    if BrowserType == BrowserTypeFlag.Chrome.value:
        ImageBrowser = webdriver.Chrome(options=options)  
    else:
        ImageBrowser = webdriver.Firefox(options=options)   
    return ImageBrowser

"""
Use webdriver access the url and use bs4 resolve page with html5 mode\
More details: https://beautifulsoup.cn/#id13
"""
def getUrl(browser,url):
    try:
        browser.get(url)
    except:
        print('please wait 120 seconds')           # 如果出现异常，则等待120s，重启读取
        # d.quit()
        time.sleep(120)
        browser.get(url)
        print('Connection Rest')
    time.sleep(1)
    sp = BeautifulSoup(browser.page_source, "html5lib")  # html5解析网页
    #browser.get('about:blank')                           # 这个很关键，防止出现链接污染
    return sp                                      # 返回解析过后的网址源码


"""
614    异世界后宫
15355  愚者之夜
9      家庭教師
"""

numComic = '9' 

url = 'https://www.mangabz.com/'+numComic+'bz/'
browser  = noImageModeBrowser()
sp = getUrl(browser,url)

# find the list_length
l = sp.find('div',{"class": "detail-list-form-con"}).find_all('a')

# find the comic's title
comicTitle = re.findall(r"[^\s]+",sp.find('p',{"class": "detail-info-title"}).text)[0]

# get the each comic url
u = []  # 55 chapter
n = []  # 20 page
t = []  # /m208433/
for o in l:
    """
    use re module extract the num
    
    l[0]:
        <a class="detail-list-form-item" href="/m208433/" target="_blank" title="">第55話                     <span>（20P）</span>                                </a>
    l[0].text:
        '第55話                     （20P）                                '     
    """
    un = re.findall(r"\d+",o.text)
    un1 = re.findall(r"[^\s]+(?=\s)",o.text)
    if len(un) != 1:
        u.append(un1[0])
        n.append(un[-1])
        t.append(o['href'])
        

"""
let's goto the next url and download each chapter of this comic

"""

class downloadImageMethod(Enum):
    humanLike  = 1
    screenShot = 2
    requestLib = 3
    

def downloadImage(pageNum,beginPageNum,chapterNum,endPageNum,floderPath,MethodFlag):
    
    with tqdm(total=endPageNum) as pbar:
        pbar.set_description('Comic Chapter'+ u[chapterNum]+'Processing')
        pbar.update(beginPageNum)
        for j in range(beginPageNum,endPageNum):
               
            comicPageUrl = 'https://www.mangabz.com'+t[chapterNum]+'#ipg'+str(j)
            
            downloadBrowser = ImageModeBrowser()
            downloadBrowser.set_window_size(50, 50)
            #downloadBrowser.maximize_window()
            
            imageSp = getUrl(downloadBrowser,comicPageUrl)
            time.sleep(random.uniform(0,0.25))
            im = imageSp.find('img',{"id": "cp_image"})
            imageUrl= im.get('src')
            
            # open new tab
            downloadBrowser.switch_to.new_window('tab')
       
            downloadBrowser.get(imageUrl)
            #SP1 = getUrl(downloadBrowser,imageUrl)
            
            # find the element of image
            IMG = downloadBrowser.find_element(By.TAG_NAME,"img")
            
            """
            Three Method can get iamge:
                first use request
                if request method is denied 
                use screenshot or simu
            ref:
                https://blog.csdn.net/weixin_43715458/article/details/101283489
            """
            imageName = str(j)+'.jpg'
            downloadImagePath = floderPath+imageName        
            if MethodFlag == downloadImageMethod.humanLike.value:
                    
                """
                Method: human-like saveimage
                advantages: high resolution;
                            jpg format;
                            small size 
                disadvantage: head webdriver;
                              not support background
                """
                # 右键点击元素
                #pyautogui.hotkey('alt', 'tab')
                action = ActionChains(downloadBrowser).move_to_element(IMG)
                action.context_click(IMG)
                action.perform()
                # 图像另存为
                pyautogui.typewrite('v')
                time.sleep(random.uniform(0.25,0.5))      
                # 将文件名传给剪贴板
                pyperclip.copy(downloadImagePath)
                # ctrl + v 粘贴文件名
                pyautogui.hotkey('ctrl', 'v')     
                pyautogui.hotkey('alt', 's') 
                # 下面操作可以不要
                time.sleep(random.uniform(0,0.25))
                pyautogui.hotkey('alt', 'y') 
                #time.sleep(random.uniform(0,0.5))
                # 验证是否下载了图片
            
            if MethodFlag == downloadImageMethod.screenShot.value:
                
                
                """
                Method: screenshot saveimage
                advantages: headless webdriver 
                            support background
                disadvantage: png format;
                              medium resolution;
                              bigger size
                """
                
                imageName = str(j)+'.png'
                downloadImagePath = floderPath+imageName  
                
                location = IMG.location
                size = IMG.size
                top,bottom,left,right = location['y'], location['y']+size['height'], location['x'], location['x']+size['width']  
                # 截取整张网页图片
                screenshot = downloadBrowser.get_screenshot_as_png()
                screenshot = Image.open(BytesIO(screenshot))
                # 将网页中需要的图片通过坐标裁剪出来 但是这样出来的图片大小更大
                screenshot = screenshot.crop((left, top, right, bottom))
                #screenshot = screenshot.convert('RGB')
                screenshot.save(downloadImagePath)      
                   
                    
            if MethodFlag == downloadImageMethod.requestLib.value:    
    
                # 请求头
                headers = {
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                }
                
                # download image
                try:
                    urllib3.disable_warnings()
                    r = requests.get(imageUrl, stream=True,headers = headers)
                    print(r.status_code) 
                except requests.exceptions.ConnectionError:
                    print('ConnectionError -- please wait 60 seconds')
                    time.sleep(120)
                    urllib3.disable_warnings()
                    r = requests.get(imageUrl, stream=True,verify=False)
                    print('Connection Rest')   
                
                if (r.status_code == 200):
                    time.sleep(random.uniform(0.5,1))
                    # save the image
                    # progess
                    totalImageSize = int(r.headers.get('content-length', 0))
                    imageName = str(j)+'.jpg'
                    downloadImagePath = floderPath+imageName
                    with open(downloadImagePath, 'wb') as f,tqdm(
                        desc=downloadImagePath,
                        total=totalImageSize,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=64,
                    ) as bar:
                        for data in r.iter_content(chunk_size=64):
                            f.write(data)     
                            bar.update(totalImageSize) 
            
                # 验证是否下载了图片
            if os.path.exists(downloadImagePath) is True:
                writePageFlag(pageNum,j)                
                #print('\n'+u[chapterNum]+"\t实际完成\t"+str(j)+"/"+str(endPageNum-1))
                pbar.update(1)
                downloadBrowser.close()         
                 
chapterLength = len(t)

# each chapter 
with tqdm(total=chapterLength) as pbar:
    pbar.set_description('Comic Processing')
    for i in range(chapterLength-1,-1,-1):
        # name the folder
        #floderPath = 'D:/comic/'+numComic+'/'+u[i]+'/'
        floderPath = 'D:\comic\\'+comicTitle+'\\'+u[i]+'\\'
        pageNum    = floderPath+'page_num.txt'
        # create the folder
        os.makedirs(floderPath, exist_ok=True)
        # check the folder
        if os.path.exists(floderPath) is True:
            #print('\n'+u[i]+'floder \t '+'has been created',end = ' \r')
            if os.path.exists(pageNum) is False:
                writePageFlag(pageNum,1)
                
            """
            About downlaod:
                We consider three condition:
                    1. have been download
                    2. No download
                    3. breakpoint download
            """
            
            downloadPageNum = readPageFlag(pageNum)
            endPageNum = int(n[i])
            # if download all?
            if downloadPageNum == endPageNum:
                pbar.update(1)
            if downloadPageNum == 1:
                #print(u[i]+'\t'+'开始下载\r',end = ' \r')
                beginPageNum = 1
                # download each page
                downloadImage(pageNum,beginPageNum,i,endPageNum,floderPath,1)
        
            # check the breakpoint and contiune download
            if downloadPageNum != 1 & downloadPageNum != int(n[i]):
                downloadBreakPageNum = readPageFlag(pageNum)  
                #print(u[i]+'\t'+'已下载'+str(downloadBreakPageNum)+'页',end = ' \r')
                beginPageNum = downloadBreakPageNum+1
                #   continue download
                downloadImage(pageNum,beginPageNum,i,endPageNum,floderPath,1)
        
        pbar.update(1)
        
        