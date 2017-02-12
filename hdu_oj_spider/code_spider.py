#coding:utf-8
import re

import lxml.html

from Downloader import Downloader

user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
def html_valid(url,ojname,problemid):
    D = Downloader(user_agent=user_agent)
    regex1 = re.compile(u'%s( |)%s([\s\S]*)博客园'%(ojname,problemid),re.IGNORECASE)
    regex2 = re.compile(u'%s( |)%s([\s\S]*)CSDN.NET'%(ojname,problemid),re.IGNORECASE)
    try:
        html = str(D(url).decode())
        tree = lxml.html.fromstring(html)
    except Exception as e:
        print 'error:'+str(e)
        return None
    title = tree.cssselect('title')[0].text_content()
    if re.search(regex1,title) or re.search(regex2, title): return html
    return None
    
def get_code(html):
    '''返回值的第一个参数代表code,第二个参数代表用什么语言提交, 0是G++,5是 Java
    '''
    try:
        tree = lxml.html.fromstring(html)
    except Exception as e:
        print "getcode_error:"+str(e)
    texts = tree.cssselect('pre')
    texts.extend(tree.cssselect('p > textarea.cpp'))
    regex0 = re.compile('^(#include([\s\S]*)main()[\d\D]+)')  #如果是代码里面一定包含 main() 函数
    regex1 = re.compile('^(#import([\s\S]*)main()[\d\D]+)')
    for text in texts:
        text = text.text_content()
        pattern0 = re.search(regex0, text)
        pattern1 = re.search(regex1, text)
        if(pattern0):
            text = pattern0.group(1)
            return [text,0] 
        if(pattern1):
            text = pattern1.group(1)
            return [text,5]
    return None

def code_spider(links,ojname,problemid):
    for link in links:
        html = html_valid(link, ojname, problemid)
        if html: 
            return get_code(html)
    return None
