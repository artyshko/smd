__addon_name__ = 'smd-lastfm'
__addon_ver__ = 'v0.1'

from kernel.controller import ConfigHandler as cf
import requests
import random

class LastFM(object):

    _cf_ = 'smd_lastfm'

    @cf.init.watch
    def __init__(self):

        self.client = self.__cl
        return self

    def __cl(self, val):
        return setattr(self,'_',val)

    def search(self, text):

        _url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={text}&api_key={self._}&format=json'
        response = requests.post(_url).json()
        data = response['results']['trackmatches']['track']
        return data

    def getInfo(self, data):

        if len(data):

            artist, track = data[0]['artist'], data[0]['name']
            _url = f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={self._}&artist={artist}&track={track}&format=json'
            response = requests.post(_url).json()
            uri = random.randint(1000000000,10000000000)
            uri = 's' + str(uri) + 't'

            try:

                info =  {
                    'uri' : uri,
                    'name' : response['track']['name'],
                    'artist' : [response['track']['artist']['name']],
                    'album' : response['track']['album']['title'],
                    'image' : response['track']['album']['image'][-1]['#text'],
                    'duration_ms' : response['track']['duration']
                }

                return info

            except:

                try:

                    dur = 0
                    try: dur = data[0]['duration']
                    except:pass

                    info =  {
                        'uri' : uri,
                        'name' : data[0]['name'],
                        'artist'  : [data[0]['artist']],
                        'album' : data[0]['name'],
                        'image' : data[0]['image'][-1]['#text'],
                        'duration_ms' : dur
                    }
                    return info

                except:
                    pass
        return None

    def get(self, text):
        return self.getInfo(self.search(text))
