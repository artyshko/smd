#!/usr/bin/python3
from __future__ import unicode_literals
import youtube_dl
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
import lxml
import os
import socket
import proxy
import json
import pickle
import contextlib
import imageio
import shutil
import time
import logging
import proxy
import status_manager
import heroku
import s1


#fix
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


class Youtube(object):

    def __init__(self, YT_API_KEY_N):

        self.__query = ''
        self.__host = 'https://www.youtube.com/'
        self.__url = self.__host + 'results?search_query='
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
        self.__result = []
        self.YT_API_KEY_N = YT_API_KEY_N

        self.s1 = s1.Client()
        GoogleAPI.loadData()
        logging.error(f"YT_API_KEY_{self.YT_API_KEY_N}")
        GoogleAPI.setKey(self.YT_API_KEY_N)


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

        text = str(text).replace('&','')

        try:
            data1 = self.getVideoFromYoutube(text)
            data2 = self.getVideoFromYoutube(text + ' Audio')
            s1 = self.s1.search(text, dur)

        except:
            pass

        self.__result, status = self.classify(data1, data2, s1, dur)

        return self.__result, status


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

            try:url = str(url).replace('com//watch','com/watch')
            except:pass

            #logging
            logging.info(f"Init YouTube")
            logging.warning(f"URL {url}")


            #logging
            logging.info(f"Create Directory")


            fullpath = os.getcwd() + '/cache'

            try:
                
                os.makedirs('cache/'+path)

                #logging
                logging.info(f"Created")
            except:
                #logging
                logging.error(f"Youtube:os.makedirs('cache/'+path)")

            #logging
            logging.info(f"Start downloading")

            if not status_manager.Manager.getStatus():
                
                self.__proxy = proxy.getProxy()
            
                ydl_opts = {
                    'outtmpl': f'{fullpath}/{filename}/{filename}',
                    'format':'best',
                    'proxy':self.__proxy['proxy']
                }
                logging.error(f"DOWNLOADING:USING_PROXY")

            else:
                ydl_opts = {
                    'outtmpl': f'{fullpath}/{filename}/{filename}',
                    'format':'best'
                }
                logging.error(f"DOWNLOADING:WITHOUT_PROXY")

            # #'source_address': f'{socket.gethostbyname(socket.getfqdn())}'
            # try:print(f'SERVER_IPv4:{socket.gethostbyname(socket.getfqdn())}')
            # except:pass            'proxy':self.__proxy['proxy']

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except:
                logging.error(f"DOWNLOADING:USING_PROXY[1]")
                #trying another one
                self.__proxy = proxy.getProxy()
                status_manager.Manager.setStatus(False)
            
                ydl_opts = {
                    'outtmpl': f'{fullpath}/{filename}/{filename}',
                    'format':'best',
                    'proxy':self.__proxy['proxy']
                }
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

            os.system(f'cp {fullpath}/{filename}/{filename} {fullpath}/{filename}/{filename}.mp4')

            #yt.download('cache/'+ path, filename=path)

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


    def classify(self, data1, data2, s1, duration=229486):

        print('DURATION:',duration)
       
        data1 = data1[:2] if len(data1) >= 2 else data1
        data2 = data2[:2] if len(data2) >= 2 else data2

        research = data2 + data1

        if duration == 0:
            return research

        result = -1
        link = None
        status = False


        for item in research:

            try:
                try:item = str(item).replace('com//watch','com/watch')
                except:pass

                item_duration = GoogleAPI.duration(item)
                diff = duration - item_duration
                diff = diff * -1 if diff < 0 else diff

                logging.warning(f'{item} {item_duration}')


            except:
                #logging
                logging.error(f"Some problems on classify loop")

                try:

                    try:item = str(item).replace('com//watch','com/watch')
                    except:pass

                    ydl_opts = {
                        'outtmpl': f'1',
                        'format':'best'
                    }

                    #'source_address': f'{socket.gethostbyname(socket.getfqdn())}'
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        dictMeta = ydl.extract_info(item, download=False)

                    item_duration = int(dictMeta['duration'])*1000
                    diff = duration - item_duration
                    diff = diff * -1 if diff < 0 else diff

                    logging.warning(f'{item} {item_duration}')

                    if (result == -1 or diff < result) and not str(dictMeta['title']).find('8D') > -1:
                        result, link = diff, item

                except:

                    logging.error(f"[1] Some problems on classify loop")
                                  
                    status_manager.Manager.setStatus(False)

                    logging.error(status_manager.Manager.getStatus())

        
        logging.error(f"1:{_result},")
        try:

            item_duration = s1['duration']*2
            diff = duration - item_duration
            diff = diff * -1 if diff < 0 else diff

            if (result == -1 or diff < result):
                result, link = s1['link'], None
                status = True
        except:

            if link:
            _result = [link] + data1 + data2
        else:
            _result = data1 + data2

        return _result, status

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

    def getGoogleAPIStatus(self):
        try:
            rep1, rep2 = '', ''

            try:
                #GoogleAPI.search('Google sucks')
                rep1 = 0
            except:rep1 = 0

            try:
                GoogleAPI.duration(GoogleAPI.YT_V_DEFAULT_URL+'lFGnsdV-sR4')
                rep2 = 1
            except:rep2 = 0

            return f'SERVER IS UP\nDEV[DL:TRUE-W:{self.YT_API_KEY_N}-API:{rep1}{rep2}]'
        except:
            return 'ALIVE'

    def testYT_D(self):
        #https://www.youtube.com/watch?v=Wch3gJG2GJ4
        res = self.download(
            url = 'https://www.youtube.com/watch?v=jhFDyDgMVUI',
            path='test',
            filename='test'
        )

        fullpath = os.getcwd() + '/cache'
        status = os.path.exists(f'{fullpath}/{res}/{res}.mp4')

        try:
           shutil.rmtree(f'{fullpath}/{res}')
        except:
           print('Error while deleting directory')

        if not status or not status_manager.Manager.getStatus():

            try:

                from telegram import BotHandler

                bot = BotHandler()
                bot.sendText(
                    chat_id=232027721,
                    text='SERVER IS DOWN\nRESTARTING!'
                )
                heroku.restart()

            except:print('NOOOO')

            print('HEROKU:RESTART')


            # 10 SEC SLEEP
            #
            # It has to make a pause and won't let to get the last message,
            # so it is probably gonna fix "the last message issue"

            time.sleep(10)

        return status




class GoogleAPI():


    YT_API_KEY = None
    YT_API_KEY_DATA = {}


    YT_API_V3_SEARCH = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q='
    YT_API_V3_VIDEOS = f'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&id='
    YT_V_DEFAULT_URL = 'https://www.youtube.com/watch?v='


    @staticmethod
    def loadData():

        try:

            with open('.youtube', 'rb') as f:
                data = pickle.load(f)

            GoogleAPI.YT_API_KEY_DATA = data

        except:
            pass


    @staticmethod
    def setKey(key):

        GoogleAPI.YT_API_KEY = GoogleAPI.YT_API_KEY_DATA[f'YT_API_KEY_{key}']
        logging.info(f"LOADED NEW KEY [...{GoogleAPI.YT_API_KEY[:20:]}...]")


    @staticmethod
    def search(query):

        #logging
        logging.info("YouTube APIv3 SEARCH")
        query = str(query).replace(' ','+')


        data = json.loads(
            requests.get(
                f'{GoogleAPI.YT_API_V3_SEARCH}{query}&key={GoogleAPI.YT_API_KEY}'
            ).text
        )['items']

        return [GoogleAPI.YT_V_DEFAULT_URL + str(video['id']['videoId']) for video in data]



    @staticmethod
    def duration(video):
        #logging
        logging.info("YouTube APIv3 VIDEO_INFO")

        video = str(video).split('watch?v=')[1]
        video = str(video).split('&')[0]


        data = json.loads(
            requests.get(
                f'{GoogleAPI.YT_API_V3_VIDEOS}{video}&key={GoogleAPI.YT_API_KEY}'
            ).text
        )['items'][0]['contentDetails']['duration']

        #google sucks
        _google_time_format = data[2:-1]

        try:

            min, sec = str(_google_time_format).split('M')
            msec = (int(sec) + (int(min) * 60)) * 1000

            return msec

        except: return 0


if __name__ == "__main__":

    print(GoogleAPI.YT_API_KEY_DATA)

    [print(i) for i in range(0,12)]
