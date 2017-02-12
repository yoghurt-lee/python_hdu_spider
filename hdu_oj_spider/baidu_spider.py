#coding:utf-8

import random
import re
from time import sleep

from bs4 import BeautifulSoup

from Downloader import Downloader


__author__='liyingang'

def get_real_links(links):
    real_links = []
    import requests
    for link in links:
        retry = 2
        while(retry>0):
            try:
                header = requests.head(link).headers
                real_links.append(header['location'])
                break
            except Exception as e:
                print str(e)
                retry-=1
                continue
    return real_links

def baidu_spider(url,user_agent=None,num_retries=5,cache=None,\
                 ojname='hdu',problemid=None,page=0):
    """进入百度页面
    """
    sleep(random.uniform(1,3))
    D = Downloader(user_agent=user_agent,num_retries=num_retries,cache=cache)
    html = str(D(url)) #调用Downloader类的__call__方法
    soup = BeautifulSoup(html) #通过BeautifulSoup来做匹配
    list_soup = soup.find('div',{'id':'content_left'})
    links = [link.get('href') for link in list_soup.findAll('a',{'class':'c-showurl'})]
    links = get_real_links(links)
    links = [link for link in links if \
             re.match('http://www.cnblogs.com/',link) or re.match('http://blog.csdn.net/', link)]
    return links

if __name__ == '__main__':
    url = 'https://www.baidu.com/s?wd=hdu1000&ct=2097152&pn=0'
    user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    baidu_spider(url, user_agent=user_agent)