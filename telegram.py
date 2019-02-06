import requests
import datetime
import io, os
import main

class BotHandler(object):

    def __init__(self):
        self.token = '752979930:AAFhdyGx0CSOJ-m17wLGN0NhrxvpwCqCPoQ'
        self.api_url = "https://api.telegram.org/bot{}/".format(self.token)

    def getUpdates(self, offset=None, timeout=30):

        method = 'getUpdates'
        params = {
            'timeout': timeout,
            'offset': offset
        }

        response = requests.get(self.api_url + method, params)

        return response.json()['result']

    def sendText(self, chat_id, text):

        params = {
            'chat_id': chat_id,
            'text': text
        }

        method = 'sendMessage'

        return requests.post(self.api_url + method, params)


    def sendAudio(self, chat_id, name, audio):

        method = 'sendAudio'

        files = {
            'audio': audio
        }

        data = {
            'chat_id' : chat_id,
            'caption': str(name)
        }

        response = requests.post(
                        self.api_url + method,
                        files=files,
                        data=data
                    )

        print(response.status_code, response.reason, response.content)

        return response.status_code


    def checkLastUpdates(self):

        result = self.getUpdates()

        return result[-1] if len(result) > 0 else None

class Controller(object):


    def __init__(self):
        self.bot = BotHandler()
        self.offset = None

        self.downlader = main.MusicDownloader()


    def classify(self, message):

        if str(message).find('open.spotify.com') > 0:
            return 'link'

        elif str(message).find(':track:') > 0:
            return 'uri'

        else:
            return 'text'


    def convertToURI(self, link):
        return "spotify:track:" + str(str(link).split('/')[-1])


    def controller(self, message, id):

        type = self.classify(message)

        if type == 'text':

            try:
                data = self.downlader.search(message)
                uri = data['uri']
                if self.downlader.downloadBySearchQuery(message):

                    self.bot.sendAudio(chat_id=id, audio=open(f"Downloads/{uri}.mp3",'rb'), name='')
                    os.remove(f"Downloads/{uri}.mp3")

                else:
                    self.bot.sendText(chat_id,text='Something went wrong:(')

            except:
                self.bot.sendText(id,text="Sorry, i can't find that")
            return True

        elif type == 'link':
            message = self.convertToURI(message)

        try:
            print(message)
            uri = str(message).split(':')[-1]
            if self.downlader.downloadBySpotifyUri(message):
                self.bot.sendAudio(chat_id=id, audio=open(f"Downloads/{uri}.mp3",'rb'), name='')
                os.remove(f"Downloads/{uri}.mp3")
            else:
                self.bot.sendText(chat_id,text='Something went wrong:(')
        except:
            self.bot.sendText(chat_id,text="Sorry, i can't find that")

        return True



    def mainloop(self):
        while True:

            self.bot.getUpdates(self.offset)

            update = self.bot.checkLastUpdates()

            if update:

                print(update)
                try:
                    update_id = update['update_id']
                    chat_id = update['message']['chat']['id']
                    chat_name = update['message']['chat']['first_name']

                    message = update['message']['text']
                    self.controller(message, chat_id)

                except:
                    try:
                        self.bot.sendText(chat_id,text='Something went wrong:(')
                    except:pass


            self.offset = update_id + 1


if __name__ == '__main__':

    controller = Controller()
    controller.mainloop()
