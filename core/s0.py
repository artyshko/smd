from bs4 import BeautifulSoup
import requests
import lxml
import urllib.request
import datetime, time
import logging
import imageio
import os

imageio.plugins.ffmpeg.download()
from moviepy.editor import *
import moviepy.editor as mp


#include loagging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-2s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)

class Client(object):

    def __init__(self):

        self.__searchURL = 'https://freemp3downloads.online/download?url='

        self.__headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
        }

        self.result = None


    def __getRawData(self, query):

        query, raw_data = str(query).replace(' ','+'), []

        response = requests.get(
                url=f'{self.__searchURL}{query}',
                headers=self.__headers
            )
        
        soup = BeautifulSoup(response.text,'lxml')

        for time, name, link in zip(
                soup.findAll(attrs={'class': 'text-muted'}),
                soup.findAll(attrs={'class': 'card-title'}),
                soup.findAll(attrs={'class': 'card-link'})
            ):

            raw_data.append(
                {
                   'time':time.text,
                   'name':name.text,
                   'link':link['href'],
                   's':0
                }
            )
        
        return raw_data


    def __getDuration(self, time):

        tt = f'00:0{time}'
        res = sum(x * int(t) for x, t in zip([3600, 60, 1], tt.split(":"))) 
        item_duration = res * 1000

        return item_duration


    def search(self, query, duration=205600):

        logging.info(f"SEARCHING:S0:START")

        result = -1
        url = None

        data1, data2 = self.__getRawData(query), self.__getRawData(f'{query} Audio')

        data1 = data1 if len(data1) <= 4 else data1[:4]
        data2 = data2 if len(data2) <= 4 else data2[:4]

        for item in data1:item['time'] = self.__getDuration(item['time'])
        for item in data2:item['time'] = self.__getDuration(item['time'])


        logging.info(f"SEARCHING:S0:ITEMS:{len(data1)+len(data2)}")


        if duration == 0:

            url = data2[0]
        
        else:

            for item in data1:

                diff = duration - item['time']
                diff = diff * -1 if diff < 0 else diff

                if (result == -1 or diff < result) and not str(item['name']).find('8D') > -1:
                    result, url = item['time'], item
            
            for item in data2:

                diff = duration - item['time']
                diff = diff * -1 if diff < 0 else diff

                if (result == -1 or diff < result) and not str(item['name']).find('8D') > -1:
                    result, url = item['time'], item

        logging.info(f"SEARCHING:S0:DONE")
        try:logging.info(f"SEARCHING:S0:DURATION:{url['time']}")
        except:pass

        return url


    def download(self, result, uri='asjdajsd2QWUDJ'):

        logging.info(f"DOWNLOADING:S0:START")

        url, results = str(result['link']).split('=')[1], []

        response = requests.get(
                url=f'{self.__searchURL}{url}',
                headers=self.__headers
            )

        soup = BeautifulSoup(response.text,'lxml')

        for link in  soup.findAll(attrs={'class': 'btn-dl'}):

            results.append(link['href'])

        try:
            fullpath = os.getcwd() + f'/cache/{uri}/'
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
        except:
            #logging
            logging.error(f"S0:os.makedirs(fullpath)")
        
        urllib.request.urlretrieve(results[0], f'{fullpath}{uri}.mp4')

        logging.info(f"DOWNLOADING:S0:DONE")

        self.convertVideoToMusic(uri)



    def convertVideoToMusic(self, uri):

        logging.info(f"CONVERTING:S0:START")

         #logging
        logging.info(f"Start converting")

        try:
            fullpath = os.getcwd() + f'/cache/{uri}/'
            if not os.path.exists(fullpath):
                os.makedirs(fullpath)
        except:
            #logging
            logging.error(f"Youtube:os.makedirs(fullpath)")

        try:

            clip = mp.VideoFileClip(f'{fullpath}{uri}.mp4').subclip()
            clip.audio.write_audiofile(f'{fullpath}{uri}.mp3', bitrate='3000k', progress_bar=False)

            logging.info(f"CONVERTING:S0:DONE")


        except Exception as e:
            logging.error(f"Youtube.convertVideoToMusic")
            return -1

        finally:
            return 0
