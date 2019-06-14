# @author mrchi
# @Time  : 2019/6/11 15:54
# @Website http://www.mrchi.cn
# @File  : mzitu_selenium.py
# @version 1.0
# -*- coding: UTF-8 -*-
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import random
import os

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
target_url = "https://www.baidu.com/link?url=_zz8LxCfmwSav6kwxmvN_qsEjLtwA518y6jf3QaqdEPqTcp7kkn8C3huH57VAnAj&wd=&eqid=a63b61400011062a000000025cff060f"


# todo 分析:
# 主页单页面数是27个 算上广告,选择css选择器能看到最后一个child
# 详情页面数,根据给的标题 正则能出来

def search_context():
    try:
        # todo Request target
        browser.get(target_url)
        print(browser.title)

        # todo processing each page
        each_page()

    except TimeoutException:
        # return search_context()
        return print("resquest error")

# todo  detail processing
def each_page():
    #processing each page
    for i in range(1, 28):
        #child page
        css = ("#pins > li:nth-child(%s) > a" % str(i))
        try:
            target_label = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, css)))
        except Exception:
            print("error occurred It could be advertising")
            continue
        # in to  child page
        target_label.click()
        # into  new windows
        switch_to_new_window()
        #last page number
        last_page = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'body > div.main > div.content > div.pagenavi > a:nth-child(7)')))
        # todo click last pages
        last_page.click()
        # re match get page number
        page_total_number = page_number()
        # into  new windows
        switch_to_new_window()
       #save path
        root = "d:\\com.mzitu\\imgae" + str(i) + "\\"
        if os.makedirs(root):
            print(root + "File Dir Created Finish!")
        else:
            print("File Dir Exist!!")
        #detail page processing
        for x in range(page_total_number):
            click_each_detail_page = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'body > div.main > div.content > div.pagenavi > a:nth-child(1) > span')))
            click_each_detail_page.click()
            time.sleep(random.randint(0, 2))
            # todo  right click on the image
            jpg = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'img')))
            actions = ActionChains(browser)
            actions.context_click(jpg)
            actions.perform()
            # #todo input v  saved
            pyautogui.keyDown("v")
            time.sleep(1)
            pyautogui.typewrite(root + str(x))
            pyautogui.keyDown("enter")
            pyautogui.keyUp("enter")
            print("Is downloading...." + browser.title)
            time.sleep(0.5)
            pyautogui.keyDown("enter")
        first_windows()
#todo first  windows
def first_windows():
    windows = browser.window_handles
    browser.switch_to.window(windows[0])

# todo  real page number
def page_number():
    return int(re.search('(\d+)', browser.title).group(1))

# todo  seitch to new windwos
def switch_to_new_window():
    windows = browser.window_handles
    browser.switch_to.window(windows[-1])
    time.sleep(random.randint(0, 3))


if __name__ == '__main__':
    search_context()
