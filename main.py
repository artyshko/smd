#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
import sys, getopt, shutil
import os

class MusicDownloader(object):


    def __init__(self):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__editor = TagEditor()


    def __downloadMusicFromYoutube(self, name, uri):

        #finding song on youtube
        self.__youtube.get(name)

        #downloading video from youtube
        self.__youtube.download(
            url=self.__youtube.getResult(),
            path=uri,
            filename=uri
        )

        #converting video to mp3 file
        self.__youtube.convertVideoToMusic(
            uri=uri
        )


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
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/.cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{fixed_name}.mp3"
            )

            #deleting cache
            try: shutil.rmtree(f".cache/{info['uri']}")
            except: pass

            return True
        else:
            return False


    def downloadBySpotifyUriFromFile(self, filename):
        try:

            with open(filename, 'r') as f:
                data = f.readlines()

        except FileNotFoundError:

            print(f'No such file or directory: "{filename}"')
            exit(2)

        #normalize
        try:data.remove('\n')
        except:pass
        links = [ str(item).replace('\n','') for item in data ]

        for i,song in zip(range(len(links)),links):
            print(f'[{i+1}] - {song}')

            try:
                self.downloadBySpotifyUri(song)
            except:
                pass


    def downloadBySpotifyUriPlaylistMode(self, playlist_uri):

        user = Spotify.User()
        playlist = user.getPlaylistTracks(playlist_uri)

        for track, i in zip(playlist,range(len(playlist))):

            print(f'Downloading {i+1} of {len(playlist)}')

            fixed_name = f'{track["artist"][0]} - {track["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name)

            self.__editor.setTags(
                filename=f'Downloads/{fixed_name}.mp3',
                data=track
            )


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
