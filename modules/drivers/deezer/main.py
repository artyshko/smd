__module_name__ = 'smd-deezer'
__version__ = '0.1'

import re, os, sys
import logging
import requests
from kernel.controller import DriverManager as cm

_logger_ = logging.getLogger(__module_name__)


class API(cm.AbstractClassAPI):

    def __init__(self):

        self.__url = 'http://api.deezer.com/'

        API.domains = [
            'www.deezer.com'
        ]

        API.routes = {
            'track':API.get_track_info,
            'album':API.get_album_info,
            'playlist':API.get_playlist_info
        }


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

            response = requests.get(f'{self.__url}/track/{API.link}').json()

            return {
                'uri' : f"D{response['id']}T",
                'name' : response['title'],
                'artist' : [response['artist']['name']],
                'album' : response['album']['title'],
                'image' : response['album']['cover_xl'],
                'duration_ms' : response['duration']
            }

        except Exception as e:

            _logger_.error(e)
            return False


    @preprocessor
    def get_album_info(self):

        try:

            response = requests.get(f'{self.__url}/album/{API.link}').json()

            alb = {
                'name':response['title'],
                'artist':response['artist']['name'],
                'copyright': None,
                'image':response['cover_xl'],
            }

            tracks = []

            for item in response['tracks']['data']:

                tracks.append({
                    'uri' : f"D{item['id']}T",
                    'name' : item['title'],
                    'artist' : [item['artist']['name']],
                    'album' : alb['name'],
                    'image' : alb['image'],
                    'preview_url' : item['preview'],
                    'duration_ms' : item['duration']
                })

            alb.setdefault(
                'tracks', tracks
            )

            return alb

        except Exception as e:

            _logger_.error(e)
            return False


    @preprocessor
    def get_playlist_info(self):

        try:

            response = requests.get(f'{self.__url}/playlist/{API.link}').json()

            '''alb = {
                'name':response['title'],
                'artist':response['artist']['name'],
                'copyright': None,
                'image':response['cover_xl'],
            }'''

            alb = {}

            tracks = []

            for item in response['tracks']['data']:

                tracks.append({
                    'uri' : f"D{item['id']}T",
                    'name' : item['title'],
                    'artist' : [item['artist']['name']],
                    'album' : item['album']['title'],
                    'image' : item['album']['cover_xl'],
                    'preview_url' : item['preview'],
                    'duration_ms' : item['duration']
                })

            alb.setdefault(
                'tracks', tracks
            )

            return alb

        except Exception as e:

            _logger_.error(e)
            return False

