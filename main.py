#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
import os

class MusicDownloader(object):


    def __init__(self):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__editor = TagEditor()


    def __downloadMusicFromYoutube(self, name):

        #finding song on youtube
        self.__youtube.get(name)

        #downloading video from youtube
        self.__youtube.download(
            url=self.__youtube.getResult(),
            path='',
            filename=name
        )

        #converting video to mp3 file
        self.__youtube.convertVideoToMusic(
            filename=name
        )

        #deleting video
        try: os.system('rm -rf .cache')
        except: pass

        try:

            pass

            return True
        except:
            return False



    def __getSongInfoFromSpotify(self, uri):

        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None


    def downloadBySpotifyUri(self, uri):

        #get info
        info = self.__getSongInfoFromSpotify(uri)

        if info:

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name)

            self.__editor.setTags(
                filename=f'Downloads/{fixed_name}.mp3',
                data=info
            )

            try:

                pass

                return True

            except:
                return False

        else:
            return False


if __name__ == '__main__':
    try:
        while True:
            md = MusicDownloader()
            md.downloadBySpotifyUri(input('[smd]>Sporify URI:'))
    except KeyboardInterrupt:
        exit(0)
