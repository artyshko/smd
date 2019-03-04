#!/usr/bin/python3
import re, os, sys
import spotify
#used for copy to clipboard
import pyperclip
#used for web scraping
from bs4 import BeautifulSoup
import requests
import webbrowser
#flask server
from flask import Flask, request
import pickle


class Spotify(object):

    class Server(object):

        app = Flask(__name__)
        code = None

        @staticmethod
        def run():

            Spotify.Server.app.run()

        @staticmethod
        def stop():

            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()

        @staticmethod
        @app.route('/', methods=['GET', 'POST'])
        def code():

            Spotify.Server.code = request.args.get('code')
            Spotify.Server.stop()

            return 'Success.'

    class User(object):

        def __init__(
                self,
                client_id = '83e4430b4700434baa21228a9c7d11c5',
                client_secret = '9bb9e131ff28424cb6a420afdf41d44a'
            ):

            self.__client_id = client_id
            self.__client_secret = client_secret
            self.__grant_type = 'authorization_code'
            self.__scope = 'user-library-read'
            self.__redirect = 'http://localhost:5000/'
            self.__urlCode = f'https://accounts.spotify.com/authorize?client_id={self.__client_id}&response_type=code&redirect_uri={self.__redirect}&scope={self.__scope}'
            self.__url = 'https://accounts.spotify.com/api/token'

            self.__getRefreshToken()
            
            self.__client = spotipy.Spotify(auth=self.__access_token)

        def __getAccessToken(self):
            #start server
            #handling the code
            webbrowser.open_new(self.__urlCode)
            Spotify.Server.run()
            self.__code = Spotify.Server.code

            self.__body_params = {
                'grant_type': self.__grant_type,
                'code': self.__code,
                'redirect_uri': self.__redirect,
                }

            #getting access_token by POST request to Spotify API
            response = requests.post(
                self.__url,
                data=self.__body_params,
                auth=(
                    self.__client_id,
                    self.__client_secret
                )
            ).json()

            self.__access_token = response['access_token']
            self.__refresh_token = response['refresh_token']

            data = {'refresh_token' : self.__refresh_token}

            with open('.spotify_refresh_token.secret', 'wb') as f:
                pickle.dump(data, f)


        def __getAccessTokenByRefreshToken(self, refresh_token):
            response = requests.post('https://accounts.spotify.com/api/token?',
                                     {
                                        'grant_type': 'refresh_token',
                                        'refresh_token': str(refresh_token),
                                        'client_id': self.__client_id,
                                        'client_secret': self.__client_secret
                                    }
                                ).json()
            self.__access_token = response['access_token']

        def __getRefreshToken(self):
            try:
                with open('.spotify_refresh_token.secret', 'rb') as f:
                    data = pickle.load(f)
                self.__getAccessTokenByRefreshToken(data['refresh_token'])
            except:
                self.__getAccessToken()


        def getPlaylistTracks(self, playlist_uri):

            total_tracks = self.__client.user_playlist(
                user=self.__client.current_user()['id'],
                playlist_id=playlist_uri
            )['tracks']['total']

            steps = int(total_tracks)/100
            steps = int(steps) + 1 if int(steps) - steps < 0 else int(steps)

            tracks = []

            for i in range(steps):

                playlist = self.__client.user_playlist_tracks(
                    user=self.__client.current_user()['id'],
                    playlist_id=playlist_uri,
                    offset = i*100
                )

                for j, item in enumerate(playlist['items']):
                    data = item['track']
                    tracks.append({
                        'uri' : str(data['uri'].split(':')[-1]),
                        'name' : data['name'],
                        'artist' : [ artist['name'] for artist in data['artists']],
                        'album' : data['album']['name'],
                        'image' : data['album']['images'][0]['url'],
                        'duration_ms':data['duration_ms']
                    })

            return tracks


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
        ).json()['access_token']

        #initialization of spotify client
        self.client = spotipy.Spotify(self.__access_token)


    def getSongInfo(self, uri):

        data = self.client.track(uri)

        return {
            'uri' : str(uri.split(':')[-1]),
            'name' : data['name'],
            'artist' : [ artist['name'] for artist in data['artists']],
            'album' : data['album']['name'],
            'image' : data['album']['images'][0]['url'],
            'duration_ms' : data['duration_ms']
        }


    def search(self, query):

        result = self.client.search(q=query, type='track', limit=1)
        try:
            data = result['tracks']['items'][0]

            return ({
                'uri' : str(data['uri'].split(':')[-1]),
                'name' : data['name'],
                'artist' : [ artist['name'] for artist in data['artists']],
                'album' : data['album']['name'],
                'image' : data['album']['images'][0]['url'],
                'duration_ms':data['duration_ms']
            })

        except:
            return False

    def getDuration(self, uri):

        data = self.client.track(uri)
        return data['duration_ms']

if __name__ == '__main__':
    sp = Spotify.User()
