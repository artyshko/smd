#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
from lastfm import LastFM
from deezer import Deezer
import sys, getopt, shutil
import os


import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-2s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)


class MusicDownloader(object):


    def __init__(self):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__editor = TagEditor()
        self.__last = LastFM()
        self.__deezer = Deezer()


    def __downloadMusicFromYoutube(self, name, uri, dur):

        #finding song on youtube
        self.__youtube.get(name, dur)

        #downloading video from youtube
        if self.__youtube.download(
            url=self.__youtube.getResult(),
            path=uri,
            filename=uri
        ):
            #converting video to mp3 file
            self.__youtube.convertVideoToMusic(
                uri=uri
            )
            return True
        else:
            return False

    def __getSongInfoFromSpotify(self, uri):

        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None

    def getData(self, uri):
        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None

    def getLastFMTags(self, name):
        return self.__last.get(name)

    def getDeezerTags(self, id):
        return self.__deezer.getSongInfo(id)

    def getYoutubeMusicInfo(self, url):
        return self.__youtube.getNameFromYoutube(url)

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
            if self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms']):

                self.__editor.setTags(
                    data=info
                )

                cachepath = os.getcwd() + '/cache'
                fullpath = os.getcwd() + '/Downloads'

                #logging
                logging.info(f'CACHEPATH {cachepath}')
                logging.info(f'FULLPATH {fullpath}')

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.png",
                    f"{fullpath}/{info['uri']}.png"
                )
                #logging
                logging.info(f"MOVE TO Downloads/{info['uri']}.png")

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                    f"{fullpath}/{info['uri']}.mp3"
                )
                #logging
                logging.info(f"MOVE TO Downloads/{info['uri']}.mp3")

                #deleting cache
                try:
                    shutil.rmtree(f"cache/{info['uri']}")
                    #logging
                    logging.info(f"DELETED cache/{info['uri']}")
                except:
                    #logging
                    logging.error(f"DELETING cache/{info['uri']}")

                return True
        return False

    def downloadBySearchQuery(self, query):

        #get info
        info = self.__spotify.search(query=query)

        if not info:
            info = self.__last.get(query)

        if info:

            #logging
            logging.info(f'SONG  {info["artist"][0]} - {info["name"]}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #logging
            logging.info(f'FIXED {fixed_name}')

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            #logging
            logging.info(f'CACHEPATH {cachepath}')
            logging.info(f'FULLPATH {fullpath}')

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.png",
                f"{fullpath}/{info['uri']}.png"
            )
            #logging
            logging.info(f"MOVE TO Downloads/{info['uri']}.png")

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{info['uri']}.mp3"
            )
            #logging
            logging.info(f"MOVE TO Downloads/{info['uri']}.mp3")

            #deleting cache
            try:
                shutil.rmtree(f"cache/{info['uri']}")
                #logging
                logging.info(f"DELETED cache/{info['uri']}")
            except:
                #logging
                logging.error(f"DELETING cache/{info['uri']}")

            return True, info
        else:
            return False, None

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

        for info, i in zip(playlist,range(len(playlist))):

            print(f'Downloading {i+1} of {len(playlist)}')

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

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{info['uri']}.mp3"
            )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

    def downloadFromYoutubeMusic(self, url, info):

        uri = info['uri']

        #downloading video from youtube
        if self.__youtube.download(
            url=url,
            path=uri,
            filename=uri
        ):

            #converting video to mp3 file
            self.__youtube.convertVideoToMusic(
                uri=uri
            )

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            #logging
            logging.info(f'CACHEPATH {cachepath}')
            logging.info(f'FULLPATH {fullpath}')

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.png",
                f"{fullpath}/{info['uri']}.png"
            )
            #logging
            logging.info(f"MOVE TO Downloads/{info['uri']}.png")

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{info['uri']}.mp3"
            )
            #logging
            logging.info(f"MOVE TO Downloads/{info['uri']}.mp3")

            #deleting cache
            try:
                shutil.rmtree(f"cache/{info['uri']}")
                #logging
                logging.info(f"DELETED cache/{info['uri']}")
            except:
                #logging
                logging.error(f"DELETING cache/{info['uri']}")

            return True, info
        else:
            return False, None

    def downloadByDeezerID(self, uri):
        #get info
        info = self.__deezer.getSongInfo(uri)

        if info:

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            if self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms']):

                self.__editor.setTags(
                    data=info
                )

                cachepath = os.getcwd() + '/cache'
                fullpath = os.getcwd() + '/Downloads'

                #logging
                logging.info(f'CACHEPATH {cachepath}')
                logging.info(f'FULLPATH {fullpath}')

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.png",
                    f"{fullpath}/{info['uri']}.png"
                )
                #logging
                logging.info(f"MOVE TO Downloads/{info['uri']}.png")

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                    f"{fullpath}/{info['uri']}.mp3"
                )
                #logging
                logging.info(f"MOVE TO Downloads/{info['uri']}.mp3")

                #deleting cache
                try:
                    shutil.rmtree(f"cache/{info['uri']}")
                    #logging
                    logging.info(f"DELETED cache/{info['uri']}")
                except:
                    #logging
                    logging.error(f"DELETING cache/{info['uri']}")

                return True
        return False

    def search(self, query):
        return self.__spotify.search(query=query)

    def getAlbum(self, uri):
        return self.__spotify.getAlbum(uri)

    def getAlbumDeezer(self, id):
        return self.__deezer.getAlbum(id)



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
