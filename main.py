from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def crawl():
    driver = webdriver.Chrome('D:\ds101-ex2\chromedriver_win32\chromedriver.exe')

    fp = open('data/exchange_rate.aud.06_2020.07_2020.csv', 'w+')
    fp.write('date,rate\n') 

    # url = 'https://portal.vietcombank.com.vn/Personal/TG/Pages/ty-gia.aspx'
    driver.get('https://portal.vietcombank.com.vn/Personal/TG/Pages/ty-gia.aspx')
    # element = WebDriverWait(driver, 10k00).until(EC.presence_of_element_located(By.ID( "txttungngay")))
    # element1 = WebDriverWait(driver, 1000).until(EC.presence_of_element_located(By.ID, ("ct100_Content_ExrateView")))

    textbox = driver.find_element_by_id('txttungay')
    day = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    # table = driver.find_elements_by_xpath("//table[@id='ct100_Content_ExrateView']") 
    table = driver.find_element_by_css_selector('#ctl00_Content_ExrateView')
    driver.implicitly_wait(20)

    list_rate = []
    list_date = []

    for i in day:
        table = driver.find_elements_by_id('ctl00_Content_ExrateView')
        j = "06"
        if(i == "31"):
            break
        else:
            textbox.clear()
            textbox.send_keys(i + '/' + j + '/' + '2020')
            textbox.send_keys(Keys.TAB)
            date = i + '/' + j + '/' + '2020'
            td = driver.find_element_by_css_selector("#ctl00_Content_ExrateView tr:nth-child(3) td:nth-child(5)")
            driver.implicitly_wait(20)
            # print(td.text)
            list_rate.append(td.text.replace(",", ""))
            list_date.append(date)

    for i in day:
        table = driver.find_elements_by_id('ctl00_Content_ExrateView')
        j = "07"
        textbox.clear()
        textbox.send_keys(i + '/' + j + '/' + '2020')
        textbox.send_keys(Keys.TAB)
        date = i + '/' + j + '/' + '2020'
        td = driver.find_element_by_css_selector("#ctl00_Content_ExrateView tr:nth-child(3) td:nth-child(5)")
        driver.implicitly_wait(20)
        # print(td.text)
        list_rate.append(td.text.replace(",", ""))
        list_date.append(date)
        list_rate = list(map(float, list_rate))

    for idx in range(len(list_date)):
        fp.write('{},{}\n'.format(list_date[idx], list_rate[idx]))
    fp.close()

# def compute_max_profit(list_exchange_rates):
#     maxProfit = 0
#     for i in range(0, len(list_exchange_rates) - 1):
#         for j in range(1, len(list_exchange_rates)):
#             profit = list_exchange_rates[j] - list_exchange_rates[i]
#             if(profit > maxProfit):
#                 maxProfit = profit
#     return maxProfit

def compute_max_profit(list_exchange_rates):
    minprice = 99999
    maxprofit = 0
    for i in range(0, len(list_exchange_rates)):
        if(list_exchange_rates[i] < minprice):
            minprice = list_exchange_rates[i]
        elif(list_exchange_rates[i] - minprice > maxprofit):
            maxprofit = list_exchange_rates[i] - minprice
    return maxprofit
            

if __name__ == "__main__":
    df = pd.read_csv('data/exchange_rate.aud.06_2020.07_2020.csv')
    list_exchange_rates = df['rate'].tolist()
    max_profit = compute_max_profit(list_exchange_rates)
    print(max_profit)

# df = pd.DataFrame(list(zip(list_date, list_rate)), columns = ['date', 'rate'])
# df.to_csv(r'D:\ds101-ex2\data\exchange_rate_aud.csv', index = False)
