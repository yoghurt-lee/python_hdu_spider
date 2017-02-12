#coding:utf-8
'''
Created on 2016年11月29日

@author: liyinggang
'''
import random
from time import sleep
import urllib

import os
from HDU import HDU
from baidu_spider import baidu_spider
from code_spider import code_spider


baseUrl = 'http://www.baidu.com/s'
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
maxpage = 4 #最大页数
ojname = 'hdu'
path ='hdu\\'
username = ''
password = ''

def submitcode(pid,lang,code):
    hdu = HDU(username,password) 
    if(hdu.login()):
        if(hdu.submit(pid, lang, code)):
            sleep(random.uniform(1,2))
            if(hdu.getstatus()):
                return True
    sleep(1,2)
    return False

def save_code(problemId,lang,code):
    filename = 'hdu'+str(problemId) +'.cpp' if lang == 0 else '.java'
    with open(path+'\\'+filename,'w') as f:
        f.write(code)
        
if __name__ == '__main__':
    if not os.path.exists(path):
        os.makedirs(path)
    
    username = 'XXX'  #账号
    password = 'XXX' #密码
    startnum=2000 #开始题号
    endnum = 2000 #结束题号
    for problemId in range(startnum,endnum+1):
        print u"已开始测试题编号:"+str(problemId)
        Accept = False
        cnt = 0
        for i in range(maxpage):
            data = {'wd':ojname +str(problemId),'pn':str(i)+'0','ct':'2097152'}
            data = urllib.urlencode(data)
            url = baseUrl+'?'+data
            print url
            links = baidu_spider(url,user_agent=user_agent,ojname=ojname,
                               problemid=str(problemId),page=i) #cache是保存的网页
            if links is None: continue
            L = code_spider(links,ojname='hdu',problemid=problemId)
            if L:
                code = L[0]
                lang = L[1]
                cnt+=1
                if(submitcode(problemId,lang,code)):
                    save_code(problemId,lang,code)
                    Accept = True
            if Accept or cnt>=10: break
        sleep(random.uniform(2,4))
    print u"程序运行结束,将在10秒后自动关闭"
    sleep(10)
