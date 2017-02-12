#coding:utf-8
'''
Created on 2016年11月29日

@author: liyinggang
'''
import cookielib, logging
from time import sleep
import urllib2, urllib, re

seed_url = "http://acm.hdu.edu.cn"
login_url = "/userloginex.php?action=login"
submit_url = "/submit.php?action=submit"
status_url ="/status.php"
class HDU:
    
    def __init__(self,username,password):
        self.username= username
        self.password = password
        self.code = None
        self.pid = 1000
        self.retry=False
        cj=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPHandler)
        #urllib2.urlopen()函数不支持验证、cookie或者其它HTTP高级功能。要支持这些功能，必须使用build_opener()函数创建自定义Opener对象。
        urllib2.install_opener(opener) #这句必须加,开始一直登录不上,但是具体为什么依旧待弄清
        self.headers ={"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36"}
        
    def login(self):
        postdata = {'username': self.username,
                    'userpass': self.password,
                    'login': 'Sign In'}
        postdata = urllib.urlencode(postdata)
        try:
            request=urllib2.Request(seed_url+login_url,postdata,self.headers)
            response = urllib2.urlopen(request, timeout=10)
            html = response.read()
            if html.find('Sign Out')==-1: 
                logging.error('login failed')
                return False
            print 'login success!'
            return True
        except:
            logging.error('login failed')
            return False
        logging.error('login failed')
        return False
        
    def getstatus(self):
        postdata = {'user': self.username,
                'lang': 0,
                'first': '',
                'pid': '',
                'status': 0}
        
        #这里好像hdu得网页做了限制,没法直接下载
        postdata = urllib.urlencode(postdata)
        status = ''
        waitstatus = ['Compiling','Queuing','Running']
        cnt = 0
        while True:
            try:
                regex = '<table[^>]+>([\s\S]*?)</table>'
                request=urllib2.Request(seed_url+status_url,postdata,self.headers)
                response = urllib2.urlopen(request, timeout=10)
                html = response.read()
                table = re.findall(regex, html)[1]
                regex = '<tr[^>]+>([\s\S]*?)</tr>'
                L = re.findall(regex, table)
                result = L[1]
                regex = str(self.username)
                flag = True
                for i in L:
                    if re.search(regex, i):
                        flag = False 
                        result = i
                        break
                #print result
                if flag: 
                    status = 'UNKNOWN ERROR'
                    break
                regex = '<font[^>]+>(.*?)</font>'
                status = re.findall(regex, result)[0]
                if status not in waitstatus or cnt>=50:
                    break
                cnt+=1
                sleep(10)
            except:
                print '程序发生错误终止'
                return False
        print 'hduoj problem '+str(self.pid)+':'+status
        if status=='Compilation Error' and self.retry==False:
            self.retry = True
            self.submit(pid=self.pid,lang=2,code=self.code)
            if self.getstatus():
                return True
        if status=='Accepted':
            return True
        return False
        
    def submit(self,pid,lang,code):
        postdata = {'problemid':pid,
                    'language' :lang,
                    'usercode' : code,
                    'check': '1'   
                }
        self.code = code
        self.pid = pid
        postdata = urllib.urlencode(postdata)
        try:   
            request=urllib2.Request(seed_url+submit_url,postdata,self.headers)
            response = urllib2.urlopen(request, timeout=10)
            sleep(1)
            if(response.code!=200 and response.code!=302):
                logging.error("submit fail!")
                return False 
        except:
            logging.error("submit fail!")
            return False
        print 'submit success!'
        return True