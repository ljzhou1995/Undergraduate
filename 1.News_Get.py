#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# python3.6
# windows7 & pycharm

# author: ljzhou

# target: http://stock.jrj.com.cn

import codecs
from urllib import request, parse
from bs4 import BeautifulSoup
import re
import time
from urllib.error import HTTPError, URLError
import sys


    # Set the recursion number to 1 million for deep crawling
sys.setrecursionlimit(1000000)

    # Disguise as a browser to avoid harmony
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
      'Chrome/51.0.2704.63 Safari/537.36'}

    # News definition
class News(object):
    def __init__(self):
        self.url = None  # The url
        self.topic = None  # The topic/title
        self.date = None  # The release date
        self.content = None  # The content/body
        self.author = None  # The author

## If the url meets the parsing requirements, then extract the page
def getNews(url):
    # Get all the elements of the page
    html = request.urlopen(url).read().decode('gb2312','ignore')
    # Extract
    soup = BeautifulSoup(html, 'html.parser')

    # Get information
    if not (soup.find('div', {'id': 'leftnews'})): return

    news = News()  # Create news object

    page = soup.find('div', {'id': 'leftnews'})

    if not (page.find('div', {'class': 'newsConTit'})): return
    topic = page.find('div', {'class': 'newsConTit'}).get_text()  # news topic/title
    news.topic = topic

    if not (page.find('div', {'id': 'IDNewsDtail'})): return
    main_content = page.find('div', {'id': 'IDNewsDtail'})  # news content/body

    content = ''

    for p in main_content.select('p'):
        content = content + p.get_text()

    news.content = content

    news.url = url  # news url
    f.write(news.topic + '\t' + news.content + '\n')

## DFS(depth first search) algorithm traverses the entire site
def dfs(url):
    global count
    print(url)

## The following sections need to modify the month to replace the crawling month
    pattern1 = '^http://stock.jrj.com.cn/2012/06\/[a-z0-9_\/\.]*$'  # Url rules that you can continue to access
    pattern2 = '^http://stock.jrj.com.cn/2012/06\/[0-9]{14}\.shtml$'  # Url rules for extracting news information
    
    # If the url has been accessed, then returns directly
    if url in visited:  return
    print(url)

    # Add the url to visited()
    visited.add(url)
    # print(visited)
    # Set the pause time to 1 second, in order to reduce the risk of being targeted by the web-masters
    # time.sleep(1)
    try:
        # If the url has not been accessed, then continue
        html = request.urlopen(url).read().decode('utf-8','ignore')
        # print(html)
        soup = BeautifulSoup(html, 'html.parser')

        if re.match(pattern2, url):
            getNews(url)
        # count += 1

        # Extract all the urls in the page
        links = soup.findAll('a', href=re.compile(pattern1))
        for link in links:
            print(link['href'])
            if link['href'] not in visited:
                dfs(link['href'])
            # count += 1
    except URLError as e:
        print(e)
        return
    except HTTPError as e:
        print(e)
        return

# print(count)
# if count > 3: return

visited = set()  # Stores the url that has been accessed

f = open('C:/news.txt', 'a+', encoding='utf-8')

## Use list to traverse all part of one month pages. 
## This operation enables the crawler to traverse all news in all pages of each month based on traversing all the urls of the current page.
urls=['http://stock.jrj.com.cn/xwk/201206/201206{}{}_{}.shtml'.format(str(i),str(j),str(k)) for i in range (0,4) for j in range(1,10) for k in range(1,6)]
for url in urls:
    if url == 'http://stock.jrj.com.cn/xwk/201206/20120631_5.shtml':        # Need to change
        dfs(url)
        break
    dfs(url)
else:
    dfs(url)
dfs(url)
