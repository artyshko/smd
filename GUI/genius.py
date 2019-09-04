import lyricsgenius
import pickle


def getLyrics(artist, song):

    def function():

        try:

            with open('.genius', 'rb') as f:
                data = pickle.load(f)

            return data['token']

        except:

            return None

    try:

        genius = lyricsgenius.Genius(function())
        genius.verbose, genius.remove_section_headers = False, True
        song = genius.search_song(song, artist)

        return song.lyrics

    except:return None

if __name__ == '__main__':
    print(getLyrics('Cage The Elephant', 'Ready To Let Go'))
