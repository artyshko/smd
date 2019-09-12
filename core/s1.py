from bs4 import BeautifulSoup
import requests
import lxml
import urllib.request
import datetime, time
import os
import logging


#include loagging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-2s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)


class Client(object):

    def __init__(self):

        self.__searchURL = 'https://music.xn--41a.ws/search/'
        self.__headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        self.result = None

    def search(self, query, duration=240000):

        logging.info(f"SEARCHING:S1:START")

        try:

            query = str(query).replace(' ','-')
            
            result = -1
            url = None
            nm = ''
            num = 0

            response = requests.get(
                url=f'{self.__searchURL}{query}/',
                headers=self.__headers
            )

            items = []

            soup = BeautifulSoup(response.text,'lxml')

            for time, name, link in zip(
                soup.findAll(attrs={'class': 'playlist-duration'}),
                soup.findAll(attrs={'class': 'playlist-name'}),
                soup.findAll(attrs={'class': 'playlist-btn-down no-ajaxy'})
            ):
                tt = str(time.text).replace(' ','')
                res = sum(x * int(t) for x, t in zip([3600, 60, 1], tt.split(":"))) 
                item_duration = res * 1000
                item = f'https://music.xn--41a.ws{link["href"]}'

                items.append(
                        {
                        'time':item_duration,
                        'name':name.text,
                        'link':item
                    }
                )
            items = items if len(items) <= 5 else items[:5]

            if not items:

                return None

            logging.info(f"SEARCHING:S1:ITEMS:{len(items)}")

            for item in items:

                diff = duration - item['time']
                diff = diff * -1 if diff < 0 else diff

                if (result == -1 or diff < result) and not str(item['name']).find('8D') > -1:
                    result, url, num, nm = diff, item['link'], item['time'], item['name']
            
            logging.info(f"SEARCHING:S1:DONE")
            logging.info(f"SEARCHING:S1:DURATION:{num}")

            return {
                'time':num,
                'name':nm,
                'link':url,
                's':1
            }

        except:

            return None

    
    def download(self, url, uri):

        logging.info(f"DOWNLOADING:S1:START")

       
        try:
            fullpath = os.getcwd() + f'/cache/{uri}/'
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
        except:
            #logging
            logging.error(f"S1:os.makedirs(fullpath)")
        
          
        urllib.request.urlretrieve(url['link'], f'{fullpath}{uri}.mp3')

        logging.info(f"DOWNLOADING:S1:DONE")


    def fromDictionary(self, dict):

        pass

