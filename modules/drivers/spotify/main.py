__module_name__ = 'smd-spotify'
__version__ = '0.1'

import re, os, sys
import time
import spotipy
import requests
import webbrowser
import pickle
import datetime
import humanize
import logging
from random import shuffle
from bs4 import BeautifulSoup
from flask import Flask, request
from kernel.controller import ConfigHandler as cf
from kernel.controller import DriverManager as cm

_logger_ = logging.getLogger(__module_name__)


class API(cm.AbstractClassAPI):

    _cf_ = 'smd_spotify'

    @cf.init.watch
    def __init__(self):

        self.__url = 'https://accounts.spotify.com/api/token'
        self.__grant_type = 'client_credentials'
        self.__body_params = {
            'grant_type': self.__grant_type
            }
        self.client = self.__cl

        API.domains = [
            'open.spotify.com',
            'oppn'
        ]

        API.routes = {
            'track':API.get_track_info,
            'album':API.get_album_info,
            'playlist':API.get_playlist_info
        }

        return self


    def __cl(self, val):

        return [setattr(self,_key_,_val_) for _key_,_val_ in val.items()] and self.__getAccessToken()


    def __getAccessToken(self):

        response = requests.post(
            self.__url,
            data=self.__body_params,
            auth=(
                self.__dict__['__client_id'],
                self.__dict__['__client_secret']
            )
        ).json()
        self.__access_token = response['access_token']
        return spotipy.Spotify(self.__access_token)


    """ AbstractClassAPI """

    def confirm_link(self, link):

        _route_ = None

        for domain in API.domains:
            result = re.search(domain, link)
            if result:
                for route in API.routes:
                    route_type = re.search(route, link)
                    if route_type:
                        _route_ = API.routes[route]
                        break
                break
        API.callback = _route_
        API.link = link

        return _route_


    def preprocessor(_function_):
        def wrapper(*args):
            API.link = str(str(API.link).split('/')[-1]).split('?')[0]
            __result__ = _function_(*args)
            return __result__
        return wrapper


    @preprocessor
    def get_track_info(self):

        try:

            data = self.client.track(API.link)

            return {
                'uri' : API.link,
                'name' : data['name'],
                'artist' : [artist['name'] for artist in data['artists']],
                'album' : data['album']['name'],
                'image' : data['album']['images'][0]['url'],
                'duration_ms' : data['duration_ms']
            }

        except Exception as e:

            _logger_.error(e)
            return False


    @preprocessor
    def get_album_info(self):

        try:

            album = self.client.album(API.link)

            copyright = None

            try:copyright = album['copyrights'][0]['text']
            except:pass

            alb = {
                'name':album['name'],
                'artist':album['artists'][0]['name'],
                'copyright':copyright,
                'image':album['images'][0]['url'],
            }

            tracks = []

            for data in album['tracks']['items']:
                tracks.append({
                    'uri' : str(data['uri'].split(':')[-1]),
                    'name' : data['name'],
                    'artist' : [ artist['name'] for artist in data['artists']],
                    'album' : alb['name'],
                    'image' : alb['image'],
                    'preview_url' : data['preview_url'],
                    'duration_ms' : data['duration_ms']
                })

            alb.setdefault(
                'tracks', tracks
            )

            return alb

        except Exception as e:

            _logger_.error(e)
            return False


    @preprocessor
    def get_playlist_info(self, link):

        link = API.link
