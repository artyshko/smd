__addon_name__ = 'smd-genius'
__addon_ver__ = 'v0.1'

from kernel.controller import ConfigHandler as cf
import lyricsgenius

class Genius(object):

    _cf_ = 'smd_genius'

    @cf.init.watch
    def __init__(self):

        self.client = lyricsgenius.Genius

        return self

    def get_lyrics(self, song, artist):

        try:
            self.client.verbose, self.client.remove_section_headers = False, True
            song = self.client.search_song(song, artist)
            return song.lyrics
        except: return None
