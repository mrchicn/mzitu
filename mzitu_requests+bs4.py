# @author mrchi
# @Time  : 2019/6/12 17:47
# @Website http://www.mrchi.cn
# @File  : mzitu_selenium.py
# @version 1.0
# -*- coding: UTF-8 -*-
import random
import time
import requests
from bs4 import BeautifulSoup
import re
import os
#todo Python3 解除警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#todo Python2 解除警告
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
    "Referer": "https://www.baidu.com/link?url=SlC7_Kj72Q9aP0UQqngbayvs_wW8bF5R48_wkdw7kJMhbKOX9ceQVb1JfPSHVnom&wd=&eqid=ddef94c900012fe8000000025d00c90e"
}

def request_target(url):
    home_html = requests.get(url=url, headers=headers,verify=False).text
    soup = BeautifulSoup(home_html, 'lxml')
    # home every on page link
    # for i in range(1, 25):
    for i in range(1, 27):
        for child_link in soup.select('#pins > li:nth-child(%s)' % str(i)):
            print("载入...第 %s 图组 数据" % i)
            print("*" * 60)
            processing_every_link(str(child_link))

def processing_every_link(link):
    #
    rematch = re.compile('<li><a href="(.*?)"\starget="_blank"><img alt="(.*?)"\s.*?"time">(.*?)</span></li>', re.S)
    results = re.findall(rematch, link)
    for url, title, times in results:
        titles = str(title).replace(" ", "").replace(",", "").replace("，", "").replace("！", "")
        print("target: %s \ntitle: %s \ntime: %s\n" % (url, titles, times))
        target_child_page(url)

def target_child_page(child_page):
    child_html = requests.get(url=child_page, headers=headers,verify=False).text
    soup = BeautifulSoup(child_html, "lxml")
    number_processing = soup.select("body > div.main > div.content > div.pagenavi > a:nth-child(7) > span")
    page_number=re.search("(\d+)",str(number_processing)).group(1)
    for number in range(1,int(page_number)+1):
        child_html = requests.get(url=child_page + "/%s" %number, headers=headers,verify=False).text
        # print(child_html)
        image_address(child_html,page_number)

def image_address(child_html,page_number):
    soup = BeautifulSoup(child_html, "lxml")
    img = soup.select("body > div.main > div.content > div.main-image > p > a > img")
    # print(img)
    rematch = re.compile('<img alt="(.*?)"\sheight="(\d+)"\ssrc="(.*?)"\swidth="(\d+)"/>]', re.S)
    results = re.findall(rematch, str(img))
    for title,height,src,width in results:
        titles = str(title).replace(" ", "").replace(",", "").replace("，", "").replace("！", "")
        img_data = requests.get(url=src,headers=headers,verify=False)
        # print(img_data.text)
        count = str(src)[-6:]
        save_path = "d:\\com.mzitu\\%s\\" % titles
        try:
            os.makedirs(save_path)
        except Exception:
            pass
        with open(save_path+count, 'wb') as f:
            f.write(img_data.content)
            time.sleep(random.randint(0,1))
            # time.sleep(0.5)
        print("正在下载 第 %s/%s 个图片 [ %s ]\t图片格式: %s x %s"%(count[:2],page_number,titles,height,width))

def all_page():
    base_url = "https://www.mzitu.com/"
    home_html = requests.get(url=base_url, headers=headers,verify=False).text
    soup = BeautifulSoup(home_html, 'lxml')
    all_page_num=soup.select("body > div.main > div.main-content > div.postlist > nav > div > a:nth-child(6)")
    rematch = re.compile('(\d+)', re.S)
    home_page_number =re.findall(rematch,str(all_page_num))[1]
    print("正在解析第 主 页数据" )
    request_target(base_url)
    for url in range(2,int(home_page_number)+1):
        child_url = base_url + "page/%s/" % url
        print("正在解析第 %s 页数据"%url)
        request_target(child_url)
        print("数据大小为:"+str(os.path.getsize("d:\\com.mzitu")))

if __name__ == '__main__':
    all_page()
