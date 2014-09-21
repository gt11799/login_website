#!/usr/bin/env python
# _*_coding=utf8 _*_
'''
Crawl the online_time of zhihu user,
Need the user name and password
store the data in the mysql
'''

import requests
import cookielib
import MySQLdb
import time
from lxml import etree

class ZhihuSpider(object):
    
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.url = 'http://www.zhihu.com/login'
        
        self.jar = cookielib.CookieJar()
        self.pwd = {
            'email':self.login,
            'password':self.password,
            'loginRedirect':'http://www.zhihu.com',
        }
        self.header = {
            'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
        }
        
    def login_zhihu(self):
        self.request = requests.get(self.url, cookies=self.jar)
        print("Geted request...")
        self.request = requests.post(self.url, headers=self.header, cookies=self.jar, data=self.pwd)
        print("Posted pwd....")
        self.parse_html()
        
    def parse_html(self):
        self.parse = etree.HTML(self.request.text)
        self.names = self.parse.xpath('//div[@class="source"]/a[@class="zg-link"]/text()')
        self.times = self.parse.xpath('//span[@class="time"]/@data-timestamp')
        assert len(self.times), "Nothing downloaded."
        self.store_name()
        
    def store_name(self):
        
        #initial mysql
        self.db = MySQLdb.connect(host="localhost", port=3307, user='user', passwd='passwd', db='zhihu')
        self.cursor = self.db.cursor()
        for item in range(len(self.times)):
            sql = "insert into login_time (name,login_time) values (%r,%r)"\
                %(self.names[item].encode('raw_unicode_escape'), self.times[item])
  
            self.cursor.execute(sql)
            
        self.db.commit()
        self.cursor.close()
        self.db.close()
        
if __name__ == '__main__':
    while True:
        spider = ZhihuSpider('user', 'passwd')
        spider.login_zhihu()
        time.sleep(600)
