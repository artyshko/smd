#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
import sys, getopt
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

            return True
        else:
            return False
    def downloadBySpotifyUriFromFile(arg):
        pass
    def downloadBySpotifyUriPlaylistMode(arg):
        pass


class CLI(object):

    @staticmethod
    def help():

        print('')
        print('\t Spotify Music Downlader (SMD)\n')
        print('./main.py [without any parameters] - normal startup\n\n')
        print('./main.py [parameter][argument] - startup with parameter\n')
        print('Parameters\n')
        print('  -h, --help       Print a help message and exit.\n')
        print('  -s, --song       Spotify song URI.\n')
        print('  -p, --playlist   Spotify playlist URI.\n')
        print('  -f, --file       File with song URIs.\n')

    @staticmethod
    def main(argv):

        try:

           opts, args = getopt.getopt(
                argv,
                "hs:p:f:",
                [
                    "help=",
                    "song=",
                    "playlist=",
                    "file="
                ])

        except getopt.GetoptError:

           CLI.help()
           sys.exit(2)

        for parameter, argument in opts:

           if parameter in ("-h", "--help"):

               CLI.help()
               sys.exit()

           elif parameter in ("-s", "--song"):

               #song uri
               try:
                   md = MusicDownloader()
                   md.downloadBySpotifyUri(argument)
               except KeyboardInterrupt:
                   exit(0)

               sys.exit()

           elif parameter in ("-p", "--playlist"):

              #playlist uri
              try:
                 md = MusicDownloader()
                 md.downloadBySpotifyUriPlaylistMode(argument)
              except KeyboardInterrupt:
                 exit(0)

              sys.exit()

           elif parameter in ("-f", "--file"):

               #from file
               try:
                  md = MusicDownloader()
                  md.downloadBySpotifyUriFromFile(argument)
               except KeyboardInterrupt:
                  exit(0)

               sys.exit()

        #normal startup
        try:
           while True:
               md = MusicDownloader()
               md.downloadBySpotifyUri(input('[smd]>Sporify URI:'))
        except KeyboardInterrupt:
           exit(0)


if __name__ == '__main__':

    CLI.main(sys.argv[1:])
