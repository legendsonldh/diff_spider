# diff_spider
This is a project which contains some different spider project about different websites.

This repository contains:

1. A sample tutorial about how to write a spider script to get what we want and the usage of the regex which are in the folder `./Tutorial`
2. Some old spider scripts which can be used in the past and can't do anything at now. Well, these so many reasons cause this situation such as the close of the website (www.pp.163.com) (www.jiandan.com) and  so on. 
3. Some spider script I use at now. Well, I will try my best to show your my code and you also can do it by yourself

## Table of Contents

- [Background](# Background)
- [Getting started and Usage](# Getting started and Usage)
- [Additional information](Additional information)

## Background

diff_spider started with the situation I faced that when I want to watch the comic,i find that lots of comics are only have put in the online comic website and if you want to from this page to the next page, you have to wait for 1-5 seconds, however when I watched the comic book, I can turn   5 pages in 10 seconds. So I considers write a spider script to collect all comic pages for my reading time. 

From the begining, I just wanted a small script until I find that it's not a easy thing to get the comic page from online comic website, so I learn other tutorial and find the solution with different questions. Time gones and I find I learned more knowledge not only usage of python, how to get the comic page, but also how to deal with the string by regex which can help me in other projects.So I think I can share what I learned with us and believe everyone can do these like me, even if the inital goal is small.

At last, I wants these spider scripts helps people who faced the same situation  with me. 

## Getting started and Usage

You should follow explanation of every script to install each dependencies. I cut some example for you:

```python
"""
-----------------------------------------------------------------
Autor:    ludeh
Time:     2022-07-30
Version:  1.0.0
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
```

Then you can run the script such as:

```python
python filename.py
```

or you can debug scripts by some IDE(VScode,Spyder,Pycharm,Python IDE and so on)

## Additional information
