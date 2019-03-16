from celery import Celery

import requests
import datetime
import io, os
import re
import main
import apple
import random
import urllib.request
import pickle

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-2s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)

manager = Celery('telegram',broker='redis://smd:mThquQxrJbyVYVlmLLAmwzLd2t5vDWVO@redis-12274.c52.us-east-1-4.ec2.cloud.redislabs.com:12274')

class BotHandler(object):

    def __init__(self):
        self.__getData()
        self.api_url = "https://api.telegram.org/bot{}/".format(self.token)

    def __getData(self):
        try:

            with open('.telegram', 'rb') as f:
                data = pickle.load(f)

            self.token = data['token']

        except:
            print('''
            A new version is available on GitHub.\n
            Download: https://github.com/artyshko/smd
            ''')
            sys.exit()

    def getUpdates(self, offset=None, timeout=30):

        method = 'getUpdates'
        params = {
            'timeout': timeout,
            'offset': offset
        }

        response = requests.get(self.api_url + method, params)
        try:
            return response.json()['result']
        except: return []

    def sendText(self, chat_id, text):

        params = {
            'chat_id': chat_id,
            'text': text
        }

        method = 'sendMessage'

        return requests.post(self.api_url + method, params)

    def sendHTML(self, chat_id, text):

        params = {
            'chat_id': chat_id,
            'parse_mode': 'HTML',
            'text': text,
        }

        method = 'sendMessage'

        return requests.post(self.api_url + method, params)


    def sendAudio(self, chat_id, name, artist, audio, thumb):

        method = 'sendAudio'

        files = {
            'audio': audio,
            'thumb':thumb
        }

        data = {
            'chat_id' : chat_id,
            'title': str(name),
            'performer':str(artist),
            'caption':f'<b>{str(artist)}</b> {str(name)}',
            'parse_mode':'HTML'
        }

        response = requests.post(
                        self.api_url + method,
                        files=files,
                        data=data
                    )
        #logging
        logging.info(f'SEND STATUS {response.status_code} {response.reason}')

        return response.status_code

    def sendPhoto(self, chat_id, photo, text):

        method = 'sendPhoto'

        files = {
            'photo': photo
        }

        data = {
            'chat_id' : chat_id,
            'caption':text,
            'parse_mode':'HTML'
        }

        response = requests.post(
                        self.api_url + method,
                        files=files,
                        data=data
                    )
        #logging
        logging.info(f'SEND STATUS {response.status_code} {response.reason}')

        return response.status_code


    def sendSticker(self, chat_id, sticker):

        method = 'sendSticker'

        files = {
            'sticker': sticker
        }

        data = {
            'chat_id' : chat_id,
        }

        response = requests.post(
                        self.api_url + method,
                        files=files,
                        data=data
                    )
        #logging
        logging.info(f'SEND STATUS {response.status_code} {response.reason}')

        return response.status_code

    def checkLastUpdates(self):

        result = self.getUpdates()

        if len(result) > 0:
            return result[-1]
        else:
            return False

class Controller(object):

    def __init__(self):
        self.bot = BotHandler()
        self.offset = None

        self.downloader = main.MusicDownloader()
        self.apple = apple.AppleMusic()


    def __restart(self):

        #logging
        logging.warning(f'Restarting a downloader')
        logging.warning(f'Trying to do the same')

        self.downloader = main.MusicDownloader()

        return True

    def __send(self, data, user, incorrect=False):

        uri, name = data['uri'], getCorrect(f'{data["artist"][0]} - {data["name"]}')

        os.rename(
            f"Downloads/{name if incorrect else uri}.mp3",
            f"Downloads/{uri if incorrect else name}.mp3"
        )

        return self.bot.sendAudio(
            chat_id=user,
            audio=open(f"Downloads/{uri if incorrect else name}.mp3",'rb'),
            thumb=open(f"Downloads/{uri}.png",'rb'),
            name=f'{data["name"]}',
            artist=f'{data["artist"][0]}'
        )

    def __remove(self, data, incorrect=False):

        uri, name = data['uri'], getCorrect(f'{data["artist"][0]} - {data["name"]}')

        #deleting song and cover
        os.remove(f"Downloads/{uri if incorrect else name}.mp3")
        #logging
        logging.info(f"DELETED Downloads/{uri if incorrect else name}.mp3")

        os.remove(f"Downloads/{uri}.png")
        #logging
        logging.info(f'DELETED Downloads/{uri}.png')

    def __sendStatus(self, user):

        self.bot.sendText(user, text='200 ALIVE')

        return True

    def __sendStartMessage(self, user):

        self.bot.sendText(
            user,
            text='https://telegra.ph/How-to-Spotify-Music-Downloader-Bot-full-instruction-03-09'
        )

        #logging
        logging.info('Hello message was sent')

        return True

    def __convertToURI(self, link):
        return "spotify:track:" + str(str(link).split('/')[-1]).split('?')[0]

    def __getTrackFromShazam(self, message):

        slug = str(message).split('/')[-1].split('-')

        message = str(message).split('I used Shazam to discover ')[1]
        message = str(message).split('. https://www.shazam.com/track/')[0]
        message = message.replace("'",'')

        song, artist, title = message, [], []
        message = str(message).split(' ')

        count = 0

        for word in message:
            count += 1 if str(word) == 'by' else 0

        if count != 1:

            try:
                for word in message:
                    try:

                        if str(word).lower().find(slug[0]) > -1:
                            title.append(word)
                            slug.pop(0)
                        else:
                            artist.append(word)

                    except:
                        artist.append(word)

                artist = " ".join(artist[1:])
                title = " ".join(title)
                song = f"{artist} - {title}"

            except:pass
            return str(song).replace('&','')

        else:

            new = []
            [new.append(word if str(word) != 'by' else '-') for word in message]
            song = " ".join(new)
            song = str(song).replace('&','')

            return str(song)



    def DL_SPOTIFY_ALBUM(self, message, user):


        link = str(message).split('?')[0]
        uri = str(link).split('/')[-1]
        data = self.downloader.getAlbum(uri)
        path = f"Downloads/{uri}.png"


        downloadAlbumImage(data['image'], path)
        logging.info(f'Downloaded {path}')

        self.bot.sendPhoto(
            chat_id=user,
            photo=open(path,'rb'),
            text=f'Album <b>{data["name"]}</b> by <b>{data["artist"]}</b>\n\n<b>{data["copyright"]}</b>'
        )

        logging.info(f'Sended {path}')
        album = data
        count = len(album['tracks'])

        for data, i in zip(album['tracks'], range(count)):
            #logging
            logging.info(f'S-ALBUM {i+1}/{count} | {data["artist"][0]} - {data["name"]}')

            if self.downloader.downloadBySpotifyUri(data['uri']):

                self.sendSong(data=data, user=user)

        os.remove(path)
        #logging
        logging.info(f'DELETED {path}')

        return True

    def DL_QUERY(self, message, user):

        state, data = self.downloader.downloadBySearchQuery(message)

        if not state:

            #in case of downloader didn't find a song
            #restarting downloader
            #and trying to get data
            self.__restart()
            state, data =  self.downloader.downloadBySearchQuery(message)


        if state:

            return self.sendSong(data=data, user=user)

        else:

            #logging
            logging.error(f'SENDED "Couldn\'t find that" MESSAGE')
            self.bot.sendSticker(user, sticker=open(f"Data/s3.webp",'rb'),)
            self.bot.sendText(user, text='Couldn\'t find that:(')

            return False

    def DL_YOUTUBE_MUSIC(self, message, user):

        self.__restart()

        link = 'http' + str(message).split('http')[-1]
        link = ''.join(str(link).split('music.')).split('&')[0]

        name = self.downloader.getYoutubeMusicInfo(link)
        tags = self.downloader.getLastFMTags(name)

        #logging
        logging.info(f"LINK {link}")
        logging.info(f"NAME {name}")

        try:

            state, data = self.downloader.downloadFromYoutubeMusic(url=link, info=tags)

            if state:

                return self.sendSong(data=data, user=user)

            else:

                #logging
                logging.warning(f"This video is unavailable.")
                self.bot.sendSticker(user, sticker=open(f"Data/s2.webp",'rb'))
                self.bot.sendText(user, text='This video is unavailable for me(')

                return False

        except:

            try:

                self.DL_QUERY(message=name, user=user)

            except:

                #logging
                logging.warning(f"This video is unavailable.")
                self.bot.sendSticker(user, sticker=open(f"Data/s2.webp",'rb'),)
                self.bot.sendText(user, text='This video is unavailable for me(')

                return False

        return True

    def DL_DEEZER_ALBUM(self, message, user):

        uri = message

        data = self.downloader.getAlbumDeezer(uri)
        path = f"Downloads/{uri}.png"


        downloadAlbumImage(data['image'], path)
        logging.info(f'Downloaded {path}')

        self.bot.sendPhoto(
            chat_id=user,
            photo=open(path,'rb'),
            text=f'Album <b>{data["name"]}</b> by <b>{data["artist"]}</b>'
        )

        logging.info(f'Sended {path}')
        album = data
        count = len(album['tracks'])

        for data, i in zip(album['tracks'], range(count)):
            #logging
            logging.info(f'D-ALBUM {i+1}/{count} | {data["artist"][0]} - {data["name"]}')

            if self.downloader.downloadByDeezerID(str(data['uri'][1:-1])):

                self.sendSong(data=data, user=user)

        os.remove(path)
        #logging
        logging.info(f'DELETED {path}')

        return True


    def sendSong(self, data, user):

        try:

            code = self.__send(data, user=user)

            if int(code) != 200:

                #trying to fix incorrect name
                code = self.__send(data, user=user, incorrect=True)

                if int(code) != 200:

                    #sending sad message
                    self.bot.sendText(user, text='Something went wrong:(')
                    self.__remove(data, incorrect=True)

                    return False

                self.__remove(data, incorrect=True)

                return True

            else:

                self.__remove(data)
                return True

        except:

            logging.error(f'ERROR IN controller.sendSong()')
            self.bot.sendText(user, text='Something went wrong:(')

            return False

    def worker(self,update):

        if 'message' in list(update.keys()):
            #in case of new message

            #get message data
            chat_id = update['message']['chat']['id']

            try:
                username = update['message']['chat']['username']
            except:
                username = 'unknown'

            if 'text' in list(update['message'].keys()):
                #skipping unsupported messages
                #get message
                message = update['message']['text']

                #logging
                logging.info(f'USER [{username}]')
                logging.info(f'MESSAGE {message}')

                try:

                    #start controller
                    self.controller(message, chat_id)

                except:
                    #logging
                    logging.error('ERROR IN CONTROLLER')

                    try:

                        self.downloader = main.MusicDownloader()
                        #restart controller
                        self.controller(message, chat_id)

                    except:

                        self.bot.sendSticker(chat_id, sticker=open(f"Data/s1.webp",'rb'))
                        self.bot.sendText(chat_id, 'Couldn\'t find that :(')

            else:
                #logging
                logging.warning('UNSUPPORTED MESSAGE')

                self.bot.sendSticker(chat_id, sticker=open(f"Data/s4.webp",'rb'))
                self.bot.sendText(chat_id, 'Wooops! Something went wrong.\nERROR CODE 42 - You are so funny!')

    def classify(self, message):

        if str(message).find('open.spotify.com') > 0:
            return 'link'

        elif str(message).find(':track:') > 0:
            return 'uri'

        elif str(message) == '/start' or str(message) == '/help':
            return 'start'

        elif str(message) == '/status':
            return 'status'

        elif str(message).find('deezer.com/track/') > 0:
            return 'dtrack'

        elif str(message).find('deezer.com/album/') > 0:
            return 'dalbum'

        else:
            return 'text'

    def controller(self, message, id):

        type = self.classify(message)

        #logging
        logging.info(f'TYPE [{type}] {message}')

        #start message
        if type == 'start':

            self.__sendStartMessage(user=id)

            return True

        elif type == 'status':

            self.bot.sendText(id, text='200 ALIVE')
            return True

        elif type == 'text':

            if str(message).find('I used Shazam to discover') > -1:

                #logging
                logging.info(f"SHAZAM SONG DETECTED")

                message = self.__getTrackFromShazam(message)

                logging.info(f"NAME {message}")

            elif str(message).find('Мое открытие на Shazam:') > -1:

                #fix for russian lang
                new = str(message).split('Мое открытие на Shazam: ')[1]
                new = str(new).split('. https')[0]
                message = new
                #logging
                logging.info(f"NAME {message}")

            elif str(message).find('youtube.com/watch') > -1:

                #logging
                logging.info(f"YOUTUBE MUSIC DETECTED")

                link = 'http' + str(message).split('http')[-1]

                if str(message).find('music.') > -1:

                    self.DL_YOUTUBE_MUSIC(message, id)

                else:

                    #logging
                    logging.warning(f"YOUTUBE SONG DETECTED")
                    self.bot.sendSticker(id,sticker=open(f"Data/s5.webp",'rb'),)
                    self.bot.sendText(id,text='You need to use YouTube Music instead of YouTube.')

                    return False

                return True

            elif str(message).find('youtu.be') > -1:

                logging.warning(f"YOUTUBE SONG DETECTED")
                self.bot.sendSticker(id,sticker=open(f"Data/s5.webp",'rb'),)
                self.bot.sendText(id,text='You need to use YouTube Music instead of YouTube.')

                return True

            elif str(message).find('itunes.apple.com') > 1:

                name = self.apple.getName(message)
                message = name

                if not name:

                    #logging
                    logging.error(f'SENDED "Couldn\'t find that" MESSAGE')
                    self.bot.sendSticker(id,sticker=open(f"Data/s3.webp",'rb'),)
                    self.bot.sendText(id,text='Couldn\'t find that:(')

                    return False

            return self.DL_QUERY(message, user=id)

        elif type == 'dtrack':

            #logging
            logging.info(f'DEEZER TRACK DETECTED')

            track = str(str(message).split('/track/')[1]).split('?')[0]
            data = self.downloader.getDeezerTags(track)

            if data:

                #logging
                logging.info(f'SONG  {data["artist"][0]} - {data["name"]}')

                if self.downloader.downloadByDeezerID(track):

                    return self.sendSong(data=data, user=id)

            else:

                #logging
                logging.error(f'SENDED "Something went wrong" MESSAGE')
                self.bot.sendSticker(id,sticker=open(f"Data/s3.webp",'rb'),)
                self.bot.sendText(id,text='Couldn\'t find that:(')

                return False

        elif type == 'dalbum':

            #logging
            logging.info(f'DEEZER ALBUM DETECTED')
            album = str(str(message).split('album/')[1]).split('?')[0]

            return self.DL_DEEZER_ALBUM(album, id)

        elif type == 'link':

            #logging
            logging.info(f'Converting open.spotify.com link to spotify URI')

            if str(message).find('/album/') > -1:

                logging.info('ALBUM MODE')
                return self.DL_SPOTIFY_ALBUM(message, user=id)

            message = self.__convertToURI(message)

        #getting data
        data = self.downloader.getData(message)

        if not data:

            #in case of downloader didn't find a song
            #restarting downloader
            #and trying to get data
            self.__restart()
            data = self.downloader.getData(message)

        if data:

            #logging
            logging.info(f'SONG  {data["artist"][0]} - {data["name"]}')

            if self.downloader.downloadBySpotifyUri(message):

                return self.sendSong(data=data, user=id)

        else:

            #logging
            logging.error(f'SENDED "Something went wrong" MESSAGE')
            self.bot.sendSticker(id,sticker=open(f"Data/s3.webp",'rb'),)
            self.bot.sendText(id,text='Couldn\'t find that:(')

            return False


def getCorrect(name):
    try:

        #checking out incorrect words
        r, text = re.compile("[а-яА-Я]+"), str(name).split(' ')
        status = True if len([w for w in filter(r.match, name)]) else False

        if status:
            return f'S{str(random.randint(1000000000,100000000000))}D'

        return re.sub(r"[\"#/@;:<>{}`+=~|.!?$%^&*№&]", string=name, repl='')

    except:

        return 'music'

def downloadAlbumImage(url, name):
    urllib.request.urlretrieve(url, name)

@manager.task
def do(update):
    controller = Controller()
    controller.worker(update)
    del controller

def mainloop():

    offset = None
    bot = BotHandler()

    while True:
        try:

            bot.getUpdates(offset)
            update = bot.checkLastUpdates()

            if update:
                update_id = update['update_id']
                offset = update_id + 1
                #celery task
                do.delay(update)
        except:
            offset = None
            bot = BotHandler()


if __name__ == '__main__':
    logging.info('Starting app')
    mainloop()
