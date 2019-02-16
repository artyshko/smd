import requests

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

            uri = '1000010000100001000010000010000101'

            try:
                uri = str(response['track']['album']['image'][-1]['#text']).split('/')[-1].split('.')[0]
            except:
                pass

            try:

                data =  {
                    'uri' : uri,
                    'name' : response['track']['name'],
                    'artist' : [response['track']['artist']['name']],
                    'album' : response['track']['album']['title'],
                    'image' : response['track']['album']['image'][-1]['#text'],
                    'duration_ms' : response['track']['duration']
                }

                return data

            except:
                pass

        return None

    def get(self, text):
        return self.getInfo(self.search(text))


if __name__ == '__main__':

    last = LastFM()
    data = last.get('Friendships (Original Mix) - Pascal')
    print(data)
