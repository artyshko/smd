#!/usr/bin/python3
import requests
import random

class LastFM(object):

    def __init__(
        self,
        api_key='a93da16045abb894cb7a4482255247bb',
        api_secret='3d50bbcc22776479ca2f4bace507b21a'
    ):

        self.__api_key = api_key
        self.__api_secret = api_secret


    def search(self, text):

        _url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={text}&api_key={self.__api_key}&format=json'

        response = requests.post(_url).json()
        data = response['results']['trackmatches']['track']

        return data

    def getInfo(self, data):

        if len(data):

            artist, track = data[0]['artist'], data[0]['name']

            _url = f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={self.__api_key }&artist={artist}&track={track}&format=json'
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


if __name__ == '__main__':

    last = LastFM()
    data = last.get('TORVA - Soma')
    print(data)
