#!/usr/bin/python3
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
import lxml
import os

#IMPORT WITH STDOUT REDIRECTION
#FIX STARTUP PYGAME HELLO MESSAGE
#THANKS @Mad Physicist FROM STACK OVERFLOW
import contextlib
# with contextlib.redirect_stdout(None):
#     from moviepy.editor import *
#     import moviepy.editor as mp

import imageio
imageio.plugins.ffmpeg.download()
from moviepy.editor import *
import moviepy.editor as mp

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-2s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)

class Youtube(object):

    def __init__(self):
        self.__query = ''
        self.__host = 'https://www.youtube.com/'
        self.__url = self.__host + 'results?search_query='
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
        self.__result = []


    def getResult(self,i=0):
        return self.__result[i]


    def getFullResult(self):
        return self.__result

    def removeInvallidLinks(self):
        temp = []
        for item in self.getFullResult():
            if 40 < len(item) < 50:
                temp.append(item)
        self.__result = temp

    def get(self, text, dur):

        data1 = self.getVideoFromYoutube(text)
        data2 = self.getVideoFromYoutube(text + ' Audio')

        self.__result = self.classify(data1, data2, dur)

        return self.__result


    def getVideoFromYoutube(self,text):
        '''
        Getting song url from YouTube
        :param text: name of song
        :return: list of results
        '''

        logging.info(f"Finding")

        request = self.__url + str(text).replace(' ','+')
        response = requests.get(request, headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')
        self.__result = []

        for link in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            self.__result.append(self.__host + link['href'])

        self.removeInvallidLinks()
        return self.__result


    def download(self, url, path='', filename='video'):
        '''
        Downloading song from YouTube
        :param url: video url on YouTube
        :param path: local directory
        :param filename: name of file
        :return: str, filename
        '''
        #logging
        logging.info(f"Start downloading")
        try:
            #logging
            logging.info(f"Init YouTube")
            logging.info(f"URL {url}")
            yt = YouTube(url)
            #logging
            logging.info(f"Get Data")
            #downloading
            yt = yt.streams.filter(
                progressive=True,
                file_extension='mp4'
            ).order_by('resolution').desc().first()

            #logging
            logging.info(f"Create Directory")


            fullpath = os.getcwd() + '/cache'

            try:
                # if not os.path.exists(fullpath):
                #     os.makedirs(fullpath)
                os.makedirs('cache/'+path)
                #logging
                logging.info(f"Created")
            except:
                #logging
                logging.error(f"Youtube:os.makedirs('cache/'+path)")

            #logging
            logging.info(f"Start downloading")


            yt.download('cache/'+ path, filename=path)

            #logging
            logging.info(f"Downloading successful")

            return filename
        except: return None


    def convertVideoToMusic(self, uri):
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

            clip = mp.VideoFileClip(f'cache/{uri}/{uri}.mp4').subclip()
            clip.audio.write_audiofile(f'cache/{uri}/{uri}.mp3', bitrate='3000k', progress_bar=False)

            logging.info(f"Converting successful")

        except Exception as e:
            logging.error(f"Youtube.convertVideoToMusic")
            return -1

        finally:
            return 0


    def getTrack(self,name):
        '''
        quick download and convert to mp3
        '''
        #self.convertVideoToMusic(self.download(self.get(name)[0],filename=name))
        return None

    def classify(self, data1, data2, duration=229486):

        data1 = data1[:2] if len(data1) >= 2 else data1
        data2 = data2[:2] if len(data2) >= 2 else data2

        research = data2 + data1

        if duration == 0:
            return research

        result = -1
        link = None

        #logging
        logging.info(f"{len(research)} research objects")

        for item in research:
            try:

                y = YouTube(item)

                item_duration = int(y.length)*1000
                diff = duration - item_duration
                diff = diff * -1 if diff < 0 else diff

                if (result == -1 or diff < result) and not str(y.title).find('8D') > -1:
                    result, link = diff, item

            except:
                #logging
                logging.error(f"Some problems on classify loop")

        if link:
            _result = [link] + data1 + data2
        else:
            _result = data1 + data2

        return _result

    def getNameFromYoutube(self, url):

        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')

        _title = soup.find('title').text
        _title = str(_title).replace(' - YouTube', '')

        _result = []
        __name = None

        if not str(_title).find('-') > -1:

            for link in soup.findAll('meta', attrs={'property': 'og:video:tag'}):
                _result.append(link.get('content'))

            if len(_result) > 1:
                name = f"{_result[0]} - {_title}"
            else:
                name = _title
        else:
            name = _title

        return name

if __name__ == "__main__":

    y = Youtube()
    name = y.getNameFromYoutube('https://youtube.com/watch?v=H4buRu9-Wb4')
    print(name)
