__addon_name__ = 'smd-tagc'
__addon_ver__ = 'v0.1'

import re, os, sys
import urllib.request
from mutagen.id3._frames import TIT2, TALB, TPE1, USLT
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error


class TagEditor(object):

    @staticmethod
    def get_image_from_spotify(url, name):

        try:
            if len(url):
                urllib.request.urlretrieve(url, name)
            else:

                cachepath = os.getcwd() + '/cache'
                datapath = os.getcwd() + '/static'
                os.system(f'cp {datapath}/temp.png {name}')
        except:
            cachepath = os.getcwd() + '/cache'
            datapath = os.getcwd() + '/static'
            os.system(f'cp {datapath}/temp.png {name}')


    @staticmethod
    def set_tags(data, lyrics=''):

        if data:

            if data['image'] == 'https://lastfm-img2.akamaized.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png':

                data['image'] = None

            if data['image'] == 'https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png':

                data['image'] = None

            TagEditor.get_image_from_spotify(data['image'], f"cache/{data['uri']}/{data['uri']}.png")
            audio = MP3(f"cache/{data['uri']}/{data['uri']}.mp3", ID3=ID3)
            audio.delete()
            audio.save()
            audio = MP3(f"cache/{data['uri']}/{data['uri']}.mp3",ID3=ID3)

            try:audio.add_tags()
            except error:pass

            audio.tags.add(APIC(3,'image/jpeg',3,'Front cover',open(f"cache/{data['uri']}/{data['uri']}.png", 'rb').read()))
            audio.tags.add(APIC(3,'image/jpeg',4,'Back cover',open(f"cache/{data['uri']}/{data['uri']}.png", 'rb').read()))
            audio.tags.add(TIT2(encoding=3,text=(data['name'])))
            audio.tags.add(TALB(encoding=3,text=(data['album'])))
            audio.tags.add(TPE1(encoding=3,text=(data['artist'][0])))
            audio.tags.add(USLT(encoding=3,lang=u'eng',desc=u'desc',text=lyrics))
            audio.save()

            ID3(f"cache/{data['uri']}/{data['uri']}.mp3").save(v2_version=3)

            return True
        else:
            return False
