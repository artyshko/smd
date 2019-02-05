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
with contextlib.redirect_stdout(None):
    import moviepy.editor as mp


class Youtube(object):

    def __init__(self):
        self.__query = ''
        self.__host = 'https://www.youtube.com/'
        self.__url = self.__host + 'results?search_query='
        self.__result = []


    def getResult(self,i=0):
        return self.__result[i]


    def getFullResult(self):
        return self.__result


    def get(self,text):
        '''
        Getting song url from YouTube
        :param text: name of song
        :return: list of results
        '''
        request = self.__url + str(text).replace(' ','+')
        response = requests.get(request)
        soup = BeautifulSoup(response.text,'lxml')
        self.__result = []

        for link in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            self.__result.append(self.__host + link['href'])

        return self.__result


    def download(self, url, path='', filename='video'):
        '''
        Downloading song from YouTube
        :param url: video url on YouTube
        :param path: local directory
        :param filename: name of file
        :return: str, filename
        '''
        yt = YouTube(url)

        #downloading
        yt = yt.streams.filter(
            progressive=True,
            file_extension='mp4'
        ).order_by('resolution').desc().first()


        fullpath = os.getcwd() + '.cache'

        if not os.path.exists(fullpath):
            os.makedirs(fullpath)

        try:
            os.makedirs('.cache/'+path)
        except: pass

        yt.download('.cache/'+ path, filename=filename)

        return filename


    def convertVideoToMusic(self, uri):

        try:

            fullpath = os.getcwd() + f'.cache/{uri}/'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            clip = mp.VideoFileClip(f'.cache/{uri}/{uri}.mp4').subclip()
            clip.audio.write_audiofile(f'.cache/{uri}/{uri}.mp3', bitrate='3000k')

        except Exception as e:
            return -1

        finally:
            return 0


    def getTrack(self,name):
        '''
        quick download and convert to mp3
        '''
        self.convertVideoToMusic(self.download(self.get(name)[0],filename=name))


if __name__ == '__main__':

    #init
    youtube = Youtube()
    name = 'Сemeteries - Leland'

    #finding song on youtube
    youtube.get(name)
    print(youtube.getResult())

    #download video from youtube
    youtube.download(
        url=youtube.getResult(),
        path='',
        filename=name
    )

    #converting video to mp3 file
    youtube.convertVideoToMusic(
        filename=name
    )

    print('done.')
