import requests

class Deezer(object):

    def __init__(self):

        '''
       Init function
       Creating deezer object
       :return: None
       '''

        self.__url = 'http://api.deezer.com/'


    def getSongInfo(self, id):

        try:

            response = requests.get(f'{self.__url}/track/{id}').json()

            return ({
                'uri' : f"D{response['id']}T",
                'name' : response['title'],
                'artist' : [response['artist']['name']],
                'album' : response['album']['title'],
                'image' : response['album']['cover_xl'],
                'duration_ms' : response['duration']
            })

        except: return None

    def getAlbum(self, id):

        try:

            response = requests.get(f'{self.__url}/album/{id}').json()

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

        except: return None

    def getPlaylist(self, id):

        try:

            response = requests.get(f'{self.__url}/playlist/{id}').json()

            alb = {
                'name':response['title']
            }

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

        except: return None

if __name__ == '__main__':

    deezer = Deezer()
    data = deezer.getSongInfo('636758392')

    print(data)
