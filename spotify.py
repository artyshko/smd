#!/usr/bin/python3
import re, os
import spotipy
#used for copy to clipboard
import pyperclip
#used for web scraping
from bs4 import BeautifulSoup
import requests


class Spotify(object):

    def __init__(
            self,
            client_id = '83e4430b4700434baa21228a9c7d11c5',
            client_secret = '9bb9e131ff28424cb6a420afdf41d44a'
        ):

        '''
       Init function
       Creating spotify object with access_token

       :param client_id: spotify client_id parametr
       :param client_secret: spotify client_secret parametr
       :return: None
       '''

        self.__url = 'https://accounts.spotify.com/api/token'
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__grant_type = 'client_credentials'
        self.__body_params = {
            'grant_type': self.__grant_type
            }

        #getting access_token by POST request to Spotify API
        self.__access_token = requests.post(
            self.__url,
            data=self.__body_params,
            auth=(
                self.__client_id,
                self.__client_secret
            )
        ).json()

        #initialization of spotify client
        self.client = spotipy.Spotify(self.__access_token['access_token'])


    def getSongInfo(self, uri):
        data = self.client.track(uri)
        return {
            'name' : data['name'],
            'artist' : [ artist['name'] for artist in data['artists']],
            'album' : data['album']['name'],
            'image' : data['album']['images'][0]['url']
        }



if __name__ == "__main__":

    spotify = Spotify()

    data = spotify.getSongInfo('spotify:track:4g5MorMCNI2aOwEBSov4RT')

    print(data)
