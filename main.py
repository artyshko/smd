#!/usr/bin/python3
from spotify import Spotify
from youtube import Youtube
from editor import TagEditor
from lastfm import LastFM
from apple import AppleMusic
from deezer import Deezer
import sys, getopt, shutil
import os, re, random
import notify2
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

        notify.send(f'Downloading from YouTube', downloaded=False)

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
            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

                notify.send(f'{info["artist"][0]} - {info["name"]}')
                return True
        return False

    def downloadBySearchQuery(self, query, path=None):

        #get info
        info = self.__spotify.search(query=query)

        if not info:
            info = self.__last.get(query)

        if info:

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')
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
                    notify.send(f'Failed to download',True)
            except:
                print('Something went wrong!')

    def downloadBySpotifyUriPlaylistMode(self, playlist_uri, path):

        user = Spotify.User()
        playlist = user.getPlaylistTracks(playlist_uri)

        for info, i in zip(playlist,range(len(playlist))):

            print(f'Downloading {i+1} of {len(playlist)}')
            
            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')

    def downloadBySpotifyUriAlbumMode(self, album_uri, path):

        user = Spotify()
        playlist = user.getAlbum(album_uri)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            info['uri'] = str(info['uri']).split('/')[-1]
            info['uri'] = str(info['uri']).split('?')[0]

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')

    def downloadByDeezerUrl(self, url, path):

        link = str(str(url).split('/')[-1]).split('?')[0]

        #get info
        info = self.__deezer.getSongInfo(link)

        if info:

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

                notify.send(f'{info["artist"][0]} - {info["name"]}')
                return True
        return False

    def downloadByDeezerUrlAlbumMode(self, album_url, path):

        link = str(str(album_url).split('/')[-1]).split('?')[0]

        #get info
        playlist = self.__deezer.getAlbum(link)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')

    def downloadByDeezerUrlPlaylistMode(self, playlist_url, path):

        link = str(str(playlist_url).split('/')[-1]).split('?')[0]

        #get info
        playlist = self.__deezer.getPlaylist(link)

        for info, i in zip(playlist['tracks'],range(len(playlist['tracks']))):

            notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')

    def downloadFromYoutubeMusic(self, url, info, path):

        print(info)

        uri = info['uri']

        notify.send(f'{info["artist"][0]} - {info["name"]}', downloaded=False)

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

            notify.send(f'{info["artist"][0]} - {info["name"]}')
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
    def help():

        CLI.logo()

        print('\t\t       Spotify Music Downloader')
        print('\t\t         version 1.7.1-stable\n')

        print(' ./main.py [argument][value] - startup with arguments\n')

        print(' Arguments:\n')

        print('        -h,  --help                  Print a help message and exit.')
        print('        -p,  --path                  Set another directory.\n')

        print('        -ss, --spotify-song          Spotify song link or URI.')
        print('        -sa, --spotify-album         Spotify album link or URI.')
        print('        -sp, --spotify-playlist      Spotify playlist URI.\n')

        print('        -ds, --deezer-song           Deezer song link.')
        print('        -da, --deezer-album          Deezer album link.')
        print('        -dp, --deezer-playlist       Deezer playlist link.\n')

        print('        -ym, --youtube-music         YouTube Music link.')
        print('        -yv, --youtube-video         YouTube Video link.\n')

        print('        -a,  --apple                 Apple Music link.')
        print('        -q,  --query                 Search query.\n')

        print(' Note that your link has to be with quotation marks - "your_url"!\n')


    @staticmethod
    def main(argv):

        array = sys.argv

        for i in range(len(array)):

            if array[i] in ('-p','--path'):
                    CLI.path = array[i+1]

                    print(CLI.path)

        #same old for loop
        for i in range(len(array)):

            if array[i] in ('-h','--help'):

                CLI.help()


            elif array[i] in ('-ss','--spotify-song'):
                try:
                    md = MusicDownloader()
                    state = md.downloadBySpotifyUri(array[i+1], CLI.path)
                    if not state:
                        notify.send(f'Failed to download',True)
                except KeyboardInterrupt:
                    sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-sa','--spotify-album'):

                try:
                   md = MusicDownloader()
                   md.downloadBySpotifyUriAlbumMode(array[i+1], CLI.path)
                except KeyboardInterrupt:
                  sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-sp','--spotify-playlist'):

                #playlist uri
                try:
                   md = MusicDownloader()
                   md.downloadBySpotifyUriPlaylistMode(array[i+1], CLI.path)
                except KeyboardInterrupt:
                  sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-ds','--deezer-song'):

                try:
                    md = MusicDownloader()
                    state = md.downloadByDeezerUrl(array[i+1], CLI.path)
                    if not state:
                        notify.send(f'Failed to download',True)
                except KeyboardInterrupt:
                    sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-da','--deezer-album'):

                try:
                   md = MusicDownloader()
                   md.downloadByDeezerUrlAlbumMode(array[i+1], CLI.path)
                except KeyboardInterrupt:
                  sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-dp','--deezer-playlist'):

                #playlist uri
                try:
                   md = MusicDownloader()
                   md.downloadByDeezerUrlPlaylistMode(array[i+1], CLI.path)
                except KeyboardInterrupt:
                  sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-ym','--youtube-music'):

                 #YouTube Music
                 try:
                     link = ''.join(str(array[i+1]).split('music.')).split('&')[0]

                     md = MusicDownloader()
                     name = md.getYoutubeMusicInfo(link)
                     tags = md.getLastFMTags(name)

                     try:
                         state = md.downloadFromYoutubeMusic(url=link, info=tags, path=CLI.path)
                     except:
                         notify.send(f'Failed to download',True)

                 except KeyboardInterrupt:
                     sys.exit(0)

                 sys.exit(0)

            elif array[i] in ('-yv','--youtube-video'):

                try:

                    md = MusicDownloader()
                    name = md.getNameFromYoutube(array[i+1])

                    uri = random.randint(1000000000,10000000000)
                    uri = 's' + str(uri) + 't'

                    info =  {
                        'uri' : uri,
                        'name' : str(name).split('-')[-1],
                        'artist' : str(name).split('-')[0],
                        'album' : 'YouTube',
                        'image' : '',
                        'duration_ms' : 0
                    }

                    state = md.downloadFromYoutubeMusic(url=array[i+1], info=info, path=CLI.path)

                    if not state:
                       notify.send(f'Failed to download',True)

                except KeyboardInterrupt:
                    sys.exit(0)
                sys.exit(0)

            elif array[i] in ('-a','--apple'):

                #Apple Music
                try:
                    md = MusicDownloader()
                    apple = AppleMusic()
                    name = apple.getName(array[i+1])
                    state = md.downloadBySearchQuery(query=name, path=CLI.path)
                    if not state:
                        notify.send(f'Failed to download',True)
                except KeyboardInterrupt:
                    sys.exit(0)

                sys.exit(0)

            elif array[i] in ('-q','--query'):

                try:
                   md = MusicDownloader()
                   state, data = md.downloadBySearchQuery(query=array[i+1], path=CLI.path)
                   if not state:
                       notify.send(f'Failed to download',True)
                except KeyboardInterrupt:
                   sys.exit(0)
                sys.exit(0)

        CLI.help()




class notify(object):

    image = os.getcwd() + '/Data/icon.png'
    sound_info = os.getcwd() + '/Data/i.mp3'
    sound_warn = os.getcwd() + '/Data/w.mp3'
    try:notify2.init("Spotify Music Downloader Notifier")
    except:pass

    @staticmethod
    def sound(error=False):
        mixer.init()
        mixer.music.load(notify.sound_warn if error else notify.sound_info)
        mixer.music.play()

    @staticmethod
    def send(message, error=False, downloaded=True):
        try:
            ns = notify2.Notification(f'{"Downloaded" if downloaded else "Start downloading"}', message=message, icon=notify.image)
            # Set the urgency level
            ns.set_urgency(notify2.URGENCY_NORMAL)
            # Set the timeout
            ns.set_timeout(5000)
            notify.sound(error)
            ns.show()
        except:pass


def getCorrect(name):
    return re.sub(r"[\"#/@;:<>{}`+=~|.!?$%^&*№&]", string=name, repl='')


if __name__ == '__main__':

    CLI.main(sys.argv[1:])
