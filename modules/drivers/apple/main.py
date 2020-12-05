__module_name__ = 'smd-apple'
__version__ = '0.1'

from bs4 import BeautifulSoup
import requests
import lxml

class AppleMusic(object):

    def __init__(self):

        # TERM has to be like "word+word+word"
        self.SEARCH_API_URL = "https://itunes.apple.com/search?entity=musicTrack&term="
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

    def __getCorrectNameFromLink(self, link):

        try:
            return str(str(str(link).split('/album/')[1]).split('/')[0]).replace('-','+')
        except: return None

    def __getRawDataFromAppleMusic(self, query):

        try:

            return requests.get(
                f"{self.SEARCH_API_URL}{query}",
                headers=self.headers
            ).json()['results']

        except: return None

    def __classify(self, results, link):

        rawLink = str(link).split('/')[-1]
        albumID, trackID = str(rawLink).split('?i=')

        try:result = results[0]
        except:result = None

        for item in results:

            if str(item['collectionId']) == albumID and str(item['trackId']) == trackID:

                result = item
                break

        return result


    def get(self, link):

        searchName = self.__getCorrectNameFromLink(link)
        results = self.__getRawDataFromAppleMusic(searchName)

        track = self.__classify(
            results=results,
            link=link
        )

        if track:

            return {
                'uri' : f"a{track['trackId']}m",
                'name' : track['trackName'],
                'artist' : [track['artistName']],
                'album' : track['collectionName'],
                'image' : str(track['artworkUrl100']).replace('100x100bb','1000x1000bb'),
                'duration_ms' : int(track['trackTimeMillis'])
            }

        else:
            return None

class AppleMusicForShazam(object):

    def __init__(self):

        # TERM has to be like "word+word+word"
        self.SEARCH_API_URL = "https://itunes.apple.com/search?entity=musicTrack&term="
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

    def __getCorrectNameFromLink(self, link):

        try:
            return str(str(link).split('/')[-1]).replace('-','+')
        except: return None

    def __getRawDataFromAppleMusic(self, query):

        try:

            return requests.get(
                f"{self.SEARCH_API_URL}{query}",
                headers=self.headers
            ).json()['results']

        except: return None

    def __classify(self, results, link):

        rawLink = str(link).split('. http')[0]
        rawLink = rawLink.lower()
        result = None

        for item in results:

            appleArtistName = str(item['artistName']).lower()
            appleTrackName = str(item['trackName']).lower()

            if str(rawLink).find(appleArtistName) > -1 and str(rawLink).find(appleTrackName) > -1:

                result = item
                break

        return result

    def __trySearchingWithArtistName(self, link):

        name = self.__getCorrectNameFromLink(link)
        artist = str(str(link).split('. http')[0]).split(' by ')[-1]
        query = f"{name}+{str(artist).replace(' ','+')}"
        result = self.__getRawDataFromAppleMusic(query)

        track = self.__classify(result, link)

        if track:

            return {
                'uri' : f"a{track['trackId']}m",
                'name' : track['trackName'],
                'artist' : [track['artistName']],
                'album' : track['collectionName'],
                'image' : str(track['artworkUrl100']).replace('100x100bb','1000x1000bb'),
                'duration_ms' : int(track['trackTimeMillis'])
            }

        else:

            return None


    def get(self, link):

        searchName = self.__getCorrectNameFromLink(link)
        results = self.__getRawDataFromAppleMusic(searchName)

        track = self.__classify(
            results=results,
            link=link
        )

        if track:

            return {
                'uri' : f"a{track['trackId']}m",
                'name' : track['trackName'],
                'artist' : [track['artistName']],
                'album' : track['collectionName'],
                'image' : str(track['artworkUrl100']).replace('100x100bb','1000x1000bb'),
                'duration_ms' : int(track['trackTimeMillis'])
            }

        else:

            return self.__trySearchingWithArtistName(link)


