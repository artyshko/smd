#!/usr/bin/python3
import re, os
import shutil
import genius
#used for mp3 ID3 tagging
from mutagen.id3._frames import TIT2, TALB, TPE1, USLT
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

#used for web scraping
import urllib.request


class TagEditor(object):

    @staticmethod
    def getImageFromSpotify(url, name):
        if len(url):
            urllib.request.urlretrieve(url, name)
        else:

            cachepath = os.getcwd() + '/cache'
            datapath = os.getcwd() + '/Data'
            os.system(f'cp {datapath}/temp.png {name}')


    @staticmethod
    def getTags():
        pass


    @staticmethod
    def setTags(data):
        '''
       Adding taggs to mp3 file

       :param filename: name of file
       :param data: dictionary with song data
                    structure of dictionary:
                    {
                        'uri' : 'str', # Song URI id
                        'name':'str', # Name of song
                        'artist':'tuple', # List of artists
                        'album':'str', # Name of album
                        'image':'str', # Url for image from Sporify
                    }

                    as example:

                    {   'uri' :  '4g5MorMCNI2aOwEBSov4RT',
                        'name': 'and then, it swallowed me',
                        'artist': ['Nohidea', 'killedmyself', 'Delta Sleep'],
                        'album': 'and then, it swallowed me',
                        'image': 'https://i.scdn.co/image/033879df...f2ddb66'
                    }

       :return: boolean, in case of some errors - False, else True
       '''
        if data:

            #download image
            TagEditor.getImageFromSpotify(data['image'], f"cache/{data['uri']}/{data['uri']}.png")


            audio = MP3(
                f"cache/{data['uri']}/{data['uri']}.mp3",
                ID3=ID3
            )

            #handle tag errors
            try:
                audio.add_tags()
            except error:
                pass

            #add a picture
            audio.tags.add(APIC(3,
                'image/jpeg',
                3,
                'Front cover',
                open(f"cache/{data['uri']}/{data['uri']}.png", 'rb').read())
            )

            #add song name
            audio.tags.add(TIT2(
                encoding=3,
                text=(data['name']))
            )

            #add song album
            audio.tags.add(TALB(
                encoding=3,
                text=(data['album']))
            )

            #add song artist
            audio.tags.add(TPE1(
                encoding=3,
                text=(data['artist'][0]))
            )

            #add song artist
            audio.tags.add(USLT(
                encoding=3,
                lang=u'eng',
                desc=u'desc',
                text=genius.getLyrics(data['artist'][0],data['name']))
            )

            #save result
            audio.save()
            ID3(f"cache/{data['uri']}/{data['uri']}.mp3").save(v2_version=3)


            return True
        else:
            return False
