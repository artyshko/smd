#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import lxml

class AppleMusic(object):

    def __init__(self):

        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }


    def get(self, url):

        url = url + '&l=uk'


        splitted = str(url).split('/')
        splitted = splitted[:3]+['ua']+splitted[4:]
        url = '/'.join(splitted)

        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text,'lxml')

        data, name, artist = None, None, None

        for link in soup.findAll('meta', attrs={'property': 'og:title'}):
            data = link.get('content')

        if str(data).find('»') > -1:
            name = str(str(data).split('», ')[0]).replace('«','')
            artist = str(data).split('», ')[1]

            song = f'{artist} - {name}'

        return song

    def getName(self, url):
        try:
            name = self.get(url)
            return name
        except:
            try:
                name = self.get(url)
                return name
            except:
                return None
if __name__ == "__main__":
    a = AppleMusic()
    a.get('https://itunes.apple.com/uk/album/simplify/1430224633?i=1430225075')
