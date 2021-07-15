import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime

# fp = open('data/melbourne.18_08_2020.22_08_2020.csv', 'w+')
# fp.write('date,time,temp,wind,humidity,barometer\n') #    date,time,temp,wind,humidity,barometer

def crawl(): 
    date = ['18', '19', '20', '21', '22']
    link = 'https://www.timeanddate.com/weather/australia/melbourne/historic?hd=202008'

    fp = open('data/melbourne.18_08_2020.22_08_2020.csv', 'w+')
    fp.write('date,time,temp,wind,humidity,barometer\n') #    date,time,temp,wind,humidity,barometer

    for i in date:
        page = requests.get(link + i, headers = {'Accept-Language': 'en-US,en;q=0.8'})
        soup = BeautifulSoup(page.content, 'html.parser')
        list_time = []
        list_temp = []
        list_baro = []
        list_wind = []
        list_humid = []
        table = soup.find(id='wt-his')
        list_tr = table.find_all('tr')
    
        for tr in list_tr:
            list_tds = tr.find_all('td')
            list_ths = tr.find_all('th')
            list_br = tr.find_all('td', 'sep')
            list_wd = tr.find_all('td', 'sep')
            list_hum = tr.find_all('td', string = re.compile("%"))

            if(len(list_tds) > 1):    
                list_time.append(list_ths[0].text.strip())
                list_temp.append(list_tds[1].text.replace('\xa0°C', ''))
                list_baro.append(list_br[1].text.replace('mbar', '').strip())
                list_wind.append(list_wd[0].text.replace('km/h', '').strip())
                list_humid.append(list_hum[0].text.replace('%', ""))

        list_time[0] = '0:00'
        list_temp = list(map(int, list_temp))
        list_baro = list(map(int, list_baro))
        list_wind = list(map(int, list_wind))

        # for i in range(len(list_temp)):
        #     list_temp[i] = int((list_temp[i] - 32) * 5 / 9)
        #     list_baro[i] = int((list_baro[i]) * 33.8639)
        #     list_wind[i] = int((list_wind[i]) * 1.609344)

        for idx in range(len(list_time)):
            time = datetime.strptime(list_time[idx], '%H:%M').strftime("%I:%M %p")
            fp.write('{},{},{},{},{},{}\n'.format(i, time.lower(), list_temp[idx], list_wind[idx], list_humid[idx], list_baro[idx]))

    fp.close()


def compute_max_temp(df):
    groups = df.groupby('date')
    return groups.max()['temp'].values.tolist()

if __name__ == "__main__":
    crawl()
    df = pd.read_csv('data/melbourne.18_08_2020.22_08_2020.csv')
    max_temp = compute_max_temp(df)
    print('{}'.format(','.join([str(t) for t in max_temp])))
    # print(df)