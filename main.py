#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
from lastfm import LastFM
from apple import AppleMusic
from deezer import Deezer
import argparse, shutil
import os, re, random
from pygame import mixer


class MusicDownloader(object):


    def __init__(self):
        self.__youtube = Youtube()
        self.__spotify = Spotify()
        self.__editor = TagEditor()
        self.__last = LastFM()
        self.__apple = AppleMusic()
        self.__deezer = Deezer()

    def __downloadMusicFromYoutube(self, name, uri, dur):

        #finding song on youtube
        self.__youtube.get(name, dur)

        print(f'Downloading from YouTube')

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

    def getNameFromYoutube(self, url):
        return self.__youtube.getNameFromYoutube(url)

    def getData(self, uri):
        try:
            return self.__spotify.getSongInfo(uri)
        except:
            return None

    def getLastFMTags(self, name):
        return self.__last.get(name)

    def getYoutubeMusicInfo(self, url):
        return self.__youtube.getNameFromYoutube(url)

    def downloadBySpotifyUri(self, uri, path):

        #get info
        info = self.__getSongInfoFromSpotify(uri)

        if info:
            print(f'{info["artist"][0]} - {info["name"]}')

            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            if self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms']):

                print(info['uri'])

                self.__editor.setTags(
                    data=info
                )

                cachepath = os.getcwd() + '/cache'
                fullpath = os.getcwd() + '/Downloads'

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

                name = f'{info["artist"][0]} - {info["name"]}'

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                    f"{fullpath}/{getCorrect(name)}.mp3"
                )

                print(path)

                if path:

                    os.rename(
                        f"{fullpath}/{getCorrect(name)}.mp3",
                        f"{path}/{getCorrect(name)}.mp3"
                    )

                #deleting cache
                try:shutil.rmtree(f"cache/{info['uri']}")
                except:pass

                print(f'{info["artist"][0]} - {info["name"]}')
                return True
        return False

    def downloadBySearchQuery(self, query, path=None):

        #get info
        info = self.__spotify.search(query=query)

        if not info:
            info = self.__last.get(query)

        if info:

            print(f'{info["artist"][0]} - {info["name"]}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try:
                shutil.rmtree(f"cache/{info['uri']}")
            except:
                pass

            print(f'{info["artist"][0]} - {info["name"]}')
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
                state = self.downloadBySpotifyUri(str(song).split(':')[-1])
                if not state:
                    print(f'Failed to download')
            except:
                print('Something went wrong!')

    def downloadBySpotifyUriPlaylistMode(self, playlist_uri, path):

        user = Spotify.User()
        playlist = user.getPlaylistTracks(playlist_uri)

        for info, i in zip(playlist,range(len(playlist))):

            print(f'Downloading {i+1} of {len(playlist)}')
            
            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            print(f'{info["artist"][0]} - {info["name"]}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            print(f'{info["artist"][0]} - {info["name"]}')

    def downloadBySpotifyUriAlbumMode(self, album_uri, path):

        user = Spotify()
        playlist = user.getAlbum(album_uri)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            print(f'{info["artist"][0]} - {info["name"]}')

            print(f'Downloading {i+1} of {len(playlist["tracks"])}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and downloading from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            print(f'{info["artist"][0]} - {info["name"]}')

    def downloadByDeezerUrl(self, url, path):

        link = str(str(url).split('/')[-1]).split('?')[0]

        #get info
        info = self.__deezer.getSongInfo(link)

        if info:

            print(f'{info["artist"][0]} - {info["name"]}')

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

                if not os.path.exists(fullpath):
                    os.makedirs(fullpath)

                name = f'{info["artist"][0]} - {info["name"]}'

                os.rename(
                    f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                    f"{fullpath}/{getCorrect(name)}.mp3"
                )

                print(path)

                if path:

                    os.rename(
                        f"{fullpath}/{getCorrect(name)}.mp3",
                        f"{path}/{getCorrect(name)}.mp3"
                    )

                #deleting cache
                try:shutil.rmtree(f"cache/{info['uri']}")
                except:pass

                print(f'{info["artist"][0]} - {info["name"]}')
                return True
        return False

    def downloadByDeezerUrlAlbumMode(self, album_url, path):

        link = str(str(album_url).split('/')[-1]).split('?')[0]

        #get info
        playlist = self.__deezer.getAlbum(link)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            print(f'{info["artist"][0]} - {info["name"]}')

            print(f'Downloading {i+1} of {len(playlist["tracks"])}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and downloading from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            print(f'{info["artist"][0]} - {info["name"]}')

    def downloadByDeezerUrlPlaylistMode(self, playlist_url, path):

        link = str(str(playlist_url).split('/')[-1]).split('?')[0]

        #get info
        playlist = self.__deezer.getPlaylist(link)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            print(f'{info["artist"][0]} - {info["name"]}')

            print(f'Downloading {i+1} of {len(playlist["tracks"])}')

            fixed_name = f'{info["artist"][0]} - {info["name"]}'
            fixed_name = fixed_name.replace('.','')
            fixed_name = fixed_name.replace(',','')
            fixed_name = fixed_name.replace("'",'')
            fixed_name = fixed_name.replace("/","")

            #finding and download from YouTube and tagging
            self.__downloadMusicFromYoutube(fixed_name, info['uri'], info['duration_ms'])

            self.__editor.setTags(
                data=info
            )

            cachepath = os.getcwd() + '/cache'
            fullpath = os.getcwd() + '/Downloads'

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try: shutil.rmtree(f"cache/{info['uri']}")
            except: pass

            print(f'{info["artist"][0]} - {info["name"]}')

    def downloadFromYoutubeMusic(self, url, info, path):

        print(info)

        uri = info['uri']

        print(f'{info["artist"][0]} - {info["name"]}')

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

            if not os.path.exists(fullpath):
                os.makedirs(fullpath)

            name = f'{info["artist"][0]} - {info["name"]}'

            os.rename(
                f"{cachepath}/{info['uri']}/{info['uri']}.mp3",
                f"{fullpath}/{getCorrect(name)}.mp3"
            )

            if path:

                os.rename(
                    f"{fullpath}/{getCorrect(name)}.mp3",
                    f"{path}/{getCorrect(name)}.mp3"
                )

            #deleting cache
            try:shutil.rmtree(f"cache/{info['uri']}")
            except:pass

            print(f'{info["artist"][0]} - {info["name"]}')
            return True, info
        else:
            return False, None

    def search(self, query):
        return self.__spotify.search(query=query)


class CLI(object):

    path = None

    @staticmethod
    def logo():

        print(u'''

_____/\\\\\\\\\\\\\\\\\\\\\\____/\\\\\\\\____________/\\\\\\\\__/\\\\\\\\\\\\\\\\\\\\\\\\____
 ___/\\\\\\/////////\\\\\\_\\/\\\\\\\\\\\\________/\\\\\\\\\\\\_\\/\\\\\\////////\\\\\\__
  __\\//\\\\\\______\\///__\\/\\\\\\//\\\\\\____/\\\\\\//\\\\\\_\\/\\\\\\______\\//\\\\\\_
   ___\\////\\\\\\_________\\/\\\\\\\\///\\\\\\/\\\\\\/_\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
    ______\\////\\\\\\______\\/\\\\\\__\\///\\\\\\/___\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
     _________\\////\\\\\\___\\/\\\\\\____\\///_____\\/\\\\\\_\\/\\\\\\_______\\/\\\\\\_
      __/\\\\\\______\\//\\\\\\__\\/\\\\\\_____________\\/\\\\\\_\\/\\\\\\_______/\\\\\\__
       _\\///\\\\\\\\\\\\\\\\\\\\\\/___\/\\\\\\_____________\/\\\\\\_\/\\\\\\\\\\\\\\\\\\\\\\\\/___
        ___\\///////////_____\\///______________\\///__\\////////////_____

        ''')

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(description="SMD")
        parser.add_argument(
        "-p",
        "--path",
        metavar="Folder",
        help="Set another directory"
        )
        parser.add_argument(
        "-ss",
        "--spotify-song",
        metavar="spotify",
        type = str,
        help="Spotify song link or URI."
        )
        parser.add_argument(
        "-sa",
        "--spotify-album",
        metavar="spotify",
        type=str,
        help="Spotify album link or URI"
        )
        parser.add_argument(
        "-sp",
        "--spotify-playlist",
        metavar="spotify",
        type=str,
        help="Spotify playlist or URI"
        )
        parser.add_argument(
        "-ds", "--deezer-song",metavar="deezer", type=str,  help="Deezer song link."
        )
        parser.add_argument(
        "-da", "--deezer-album", metavar="deezer", type=str,  help="Deezer album link"
    )
        parser.add_argument(
        "-dp", "--deezer-playlist", metavar="deezer", type=str,  help="Deezer playulist link."
        )
        parser.add_argument(
        "-ym", "--youtube-music", metavar="yt", type=str,  help="Youtube Music link"
        )
        parser.add_argument(
        "-yv", "--youtube-video", metavar="yt", type=str,  help="Youtube Video link."
        )
        parser.add_argument(
        "-a", "--apple-music", metavar="apple", type=str,  help="Apple Music Link."
        )
        parser.add_argument(
        "-q", "--query", metavar="search", type=str, help="Search query."
        )

        return parser

    @staticmethod
    def main():
        parser = CLI.get_parser()
        args = parser.parse_args()
        md = MusicDownloader()

        if args.path:
            CLI.path = args.path
            print("Path has been set to :" , args.path)

        if args.spotify_song:
            state = md.downloadBySpotifyUri(args.spotify_song, CLI.path)
            if not state:
                print(f'Failed to download')

        elif args.spotify_album:
            md.downloadBySpotifyUriAlbumMode(args.spotify_album, CLI.path)

        elif args.spotify_playlist:
            md.downloadBySpotifyUriPlaylistMode(args.spotify_playlist, CLI.path)

        elif args.deezer_song:
            state = md.downloadByDeezerUrl(args.deezer_song, CLI.path)
            if not state:
                print(f'Failed to download')

        elif args.deezer_album:
            md.downloadByDeezerUrlAlbumMode(args.deezer_album, CLI.path)

        elif args.deezer_playlist:
            md.downloadByDeezerUrlPlaylistMode(args.deezer_playlist, CLI.path)

        elif args.youtube_music:
            link = ''.join(str(args.youtube_music).split('music.')).split('&')[0]

            name = md.getYoutubeMusicInfo(link)
            tags = md.getLastFMTags(name)

        elif args.youtube_video:
            name = md.getNameFromYoutube(args.youtube_video)

            uri = random.randint(1000000000,1000000000)
            uri = 's' + str(uri) + 't'

            info =  {
            'uri' : uri,
            'name' : str(name).split('-')[-1],
            'artist' : str(name).split('-')[0],
            'album' : 'YouTube',
            'image' : '',
            'duration_ms' : 0
                }

            state = md.downloadFromYoutubeMusic(url=args.youtube_video, info=info, path=CLI.path)

            if not state:
                print(f'Failed to download')

        elif args.apple_music:
            apple = AppleMusic()
            name = apple.getName(args.apple_music)
            state = md.downloadBySearchQuery(query=name, path=CLI.path)
            if not state:
                print(f'Failed to download')

        elif args.query:
            md = MusicDownloader()
            state, data = md.downloadBySearchQuery(query=args.query, path=CLI.path)
            if not state:
                print(f'Failed to download')
    
        else:
            parser.print_help()


def getCorrect(name):
    return re.sub(r"[\"#/@;:<>{}`+=~|.!?$%^&*№&]", string=name, repl='')


if __name__ == '__main__':

    CLI.main()
