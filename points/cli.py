__point__ = 'CLI'

from kernel import controller
from kernel.smdc.core import CORE
from modules.addons import genius

class POINT():

    _cf_ = 'CLI'

    @controller.ConfigHandler.init.watch
    def __init__(self, args):

        self.args = args[1:]
        self.client = self.__cl
        return self

    def __cl(self, val):

        self.header = val

    def info(self):

        print(self.header)
        print('\t\t       Spotify Music Downloader')
        print(f'\t\t\t   version {controller.__version__}')
        print(f'\t\t\t  SMDC {CORE.VERSION}\n')

    def run(self):

        self.info()

        link = self.args[0]
        print('\n\t',link,'\n')
        data = None

        with controller.DriverManager() as drv:

            drv.create_api_context(link)
            data = drv.context.callback()

        with controller.DownloadManager() as dm:

            dm.set_lyrics_manager(genius.Genius)
            dm.get_api_callback(data)
            dm.download()
