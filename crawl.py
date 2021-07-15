from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib3
import os

# ChromeDriver Location
driver = webdriver.Chrome("chromedriver_win32\chromedriver.exe")

save_path = '/data'

list_num = list(map(str, list(range(69))))

path = "https://www.cancerresearchuk.org/about-cancer/cancer-chat/posts"

# fp = open('immotherapies.csv', 'w+', encoding="utf-8")
# fp.write('ID,user,date,immothrerapy/ies,content\n')

lst_post_id = []
lst_user = []
lst_content = []
lst_date = []
lst_state = []

try:
    for i in list_num:
        tmp = path + "?query=immunotherapies&page=0%2C" + i
        # tmp = "https://www.cancerresearchuk.org/about-cancer/cancer-chat/posts?query=immunotherapies&page=0%2C0"
        driver.get(tmp)

        main = driver.find_element_by_id("block-system-main")
        threads = main.find_elements_by_class_name("thread-title")
        for thread in threads:
            header = thread.find_element_by_tag_name("a")
            link = header.get_attribute("href")
            num = link.split("/")
            req = urllib3.PoolManager()
            res = req.request('GET', link)
            soup = bs(res.data, 'html.parser')

            # if int(num[6]) == 446631:
            post = soup.find_all(class_="post-content-inner")
            name = soup.find_all(class_="username")
            
            lst_post = []
            j = 2
            
            for span in post:
                lst_post.append(span.text)
                user = name[j].text
                j += 1
                # lst = lst_post.split("\n")
                for mini in lst_post:
                    mini = mini.split("\n")
                    
                    lst_user.append(user)
                    # for n in lst:
                    post_id = num[6]
                    lst_post_id.append(post_id)
                    
                    content = mini[4].replace("Report this post", "").strip("\n")
                    lst_content.append(content)

                    date = mini[1]
                    lst_date.append(date)

                    if "immunotherapies" in span.text or "immunotherapy" in span.text:
                        state = "Yes"
                    else:
                        state = "No"
                    lst_state.append(state)

                    # fp.write('{},{},{},{},{}\n'.format(post_id, user, date, state, content))
                    # print(lst_post_id)
                    # print(lst_user)
                    # print(lst_content)
                    # print(lst_date)
                    # print(lst_state)
                    
    print(len(lst_post_id))
    print(len(lst_user))
    print(len(lst_content))
    print(len(lst_date))
    print(len(lst_state))


finally:
    driver.quit()
    # fp.close()

# print(main.text)
# print(driver.page_source)
