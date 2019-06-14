#@author mrchi
#@Time  : 2019/6/14 12:00
#@Website http://www.mrchi.cn
#@File  : multi_thread_mzitu.py
#@version 1.0

import random
from threading import Thread
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

def request_target(Thread,*page_num):
    if len(page_num)==0:
        page_num="主"
    # print(len(page_num))
    home_html = get_url(Thread)
    soup = BeautifulSoup(home_html, 'lxml')
    # 每一页的图组链接
    for i in range(1, 27):
        for child_link in soup.select('#pins > li:nth-child(%s)' % str(i)):
            print("载入...第 [ %s ] 页 第 %s 图组 数据" %(page_num[0] ,i))
            print("*" * 60)
            processing_every_link(str(child_link))

def processing_every_link(link):
    #处理具体每个图组
    rematch = re.compile('<li><a href="(.*?)"\starget="_blank"><img alt="(.*?)"\s.*?"time">(.*?)</span></li>', re.S)
    results = re.findall(rematch, link)
    #每个具体图组的 url 标题 和 上传时间
    for url, title, times in results:
        #去掉难以识别的字符
        titles = str(title).replace(" ", "").replace(",", "").replace("，", "").replace("！", "")
        print("target: %s \ntitle: %s \ntime: %s\n" % (url, titles, times))
        target_child_page(url)

def target_child_page(child_page):
    child_html = get_url(child_page)
    soup = BeautifulSoup(child_html, "lxml")
    number_processing = soup.select("body > div.main > div.content > div.pagenavi > a:nth-child(7) > span")
    #每个图组的数量

    page_number=re.search("(\d+)",str(number_processing)).group(1)

    for number in range(1,int(page_number)+1):
        # child_html = requests.get(url=child_page + "/%s" %number, headers=headers,verify=False).text
        child_html = get_url(child_page + "/%s" %number)
        # print(child_html)
        image_address(child_html,page_number)

def image_address(child_html,page_number):
    soup = BeautifulSoup(child_html, "lxml")
    img = soup.select("body > div.main > div.content > div.main-image > p > a > img")
    # print(img)
    rematch = re.compile('<img alt="(.*?)"\sheight="(\d+)"\ssrc="(.*?)"\swidth="(\d+)"/>]', re.S)
    results = re.findall(rematch, str(img))

    for title,height,src,width in results:
        titles = str(title).replace(" ", "").replace(",", "").replace("，", "").replace("！", "").replace(".","").replace("（","").replace("）","").replace("-","").replace("：","").replace("かなえ","")
        img_data = requests.get(url=src,headers=headers,verify=False)
        # 取链接中图片标题后的数字
        file_suffix_name = str(src[-17:]).replace("/","")
        # 保存路径文件夹
        save_path = "d:\\com.mzitu.multi\\%s\\" % titles
        try:
            flag = os.path.exists(save_path)
            if not flag:
                os.makedirs(save_path)
        except Exception as e:
            print(e)
        with open(save_path+file_suffix_name, 'wb') as f:
            f.write(img_data.content)
            time.sleep(random.randint(0,2))
            # time.sleep(0.5)
        print("正在下载 第 %s/%s 个图片 [ %s ]\t图片格式: %s x %s\n"%(str(src[-6:]).replace(".jpg",""),page_number,titles,height,width))

def all_page():
    #主页
    base_url = "https://www.mzitu.com/"
    home_html = get_url(base_url)
    soup = BeautifulSoup(home_html, 'lxml')
    all_page_num=soup.select("body > div.main > div.main-content > div.postlist > nav > div > a:nth-child(6)")
    rematch = re.compile('(\d+)', re.S)
    #共有多少页
    home_page_number =re.findall(rematch,str(all_page_num))[1]
    # print("正在解析第 主 页数据\n" )
    # request_target(base_url)
    for url in range(2,int(home_page_number)+1):
        child_url = base_url + "page/%s/" % url
        print("正在解析第 %s 页数据\n"%url)
        # request_target(child_url)
        #启动多线程
        t=Thread(target=request_target,args=(child_url,url,))
        t.start()
        time.sleep(5)
        print("[当前时间:%s]\n"%time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


def get_url(base_url):
    time.sleep(3)
    home_html = requests.get(url=base_url, headers=headers, verify=False).text
    return home_html

if __name__ == '__main__':
    all_page()
