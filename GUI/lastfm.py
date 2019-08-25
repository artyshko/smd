#!/usr/bin/python3
import requests
import random
import humanize

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

    def searchArtist(self, text):

        _url = f'http://ws.audioscrobbler.com/2.0/?method=artist.search&artist={text}&api_key={self.__api_key}&format=json'

        response = requests.post(_url).json()
        data = response['results']['artistmatches']['artist'][0]

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

    def getArtistsInfo(self, text=None):

        _url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={text}&api_key={self.__api_key}&format=json'

        response = requests.post(_url).json()

        listeners = humanize.intword(response['artist']['stats']['listeners'])
        pl_count = humanize.intword(response['artist']['stats']['playcount'])

        if str(listeners).isdigit():

            listeners = humanize.intcomma(response['artist']['stats']['listeners'])
        
        if str(pl_count).isdigit():

            pl_count = humanize.intcomma(response['artist']['stats']['playcount'])


        data = {
            'listeners':response['artist']['stats']['listeners'],
            'listeners_display':listeners,
            'playcount':response['artist']['stats']['playcount'],
            'playcount_display':pl_count,
            'bio':str(response['artist']['bio']['content']).split('<a href="')[0]
        }

        return data


if __name__ == '__main__':

    last = LastFM()
    data = last.getArtistsInfo('The Neighbourhood')
    print(data)