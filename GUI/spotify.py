#!/usr/bin/python3
import re, os, sys
import spotipy
#used for web scraping
from bs4 import BeautifulSoup
import requests
import webbrowser
#flask server
from flask import Flask, request
import pickle
from random import shuffle
import time
import datetime
import humanize


class Spotify(object):

    class Server(object):

        app = Flask(__name__)
        code = None


        @staticmethod
        def run():

            Spotify.Server.app.run()


        @staticmethod
        def stop():

            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()


        @staticmethod
        @app.route('/', methods=['GET', 'POST'])
        def getCode():

            Spotify.Server.code = request.args.get('code')
            Spotify.Server.stop()

            return 'Success.'

    class User(object):

        def __init__(self, server):

            self.__grant_type = 'authorization_code'
            self.__scope = '''
                user-library-read,
                user-top-read,
                user-follow-read,
                playlist-read-private,
                playlist-read-collaborative,
                user-read-recently-played
            '''
            self.server = server
            self.__getData()
            self.__redirect = 'http://localhost:5000/'
            self.__urlCode = f'https://accounts.spotify.com/authorize?client_id={self.__client_id}&response_type=code&redirect_uri={self.__redirect}&scope={self.__scope}'
            self.__url = 'https://accounts.spotify.com/api/token'
            self.__image = 'https://raw.githubusercontent.com/artyshko/smd/telegram/Data/9.png'

            if not self.server:

                self.__getRefreshToken()

                self.__client = spotipy.Spotify(auth=self.__access_token)
            
            
        def getURL(self):

            return self.__urlCode

        def serverLogin(self, code):

            self.__code = code

            self.__body_params = {
                'grant_type': self.__grant_type,
                'code': self.__code,
                'redirect_uri': self.__redirect,
                }

            #getting access_token by POST request to Spotify API
            response = requests.post(
                self.__url,
                data=self.__body_params,
                auth=(
                    self.__client_id,
                    self.__client_secret
                )
            ).json()

            self.__access_token = response['access_token']
            self.__refresh_token = response['refresh_token']

            data = {'refresh_token' : self.__refresh_token}

            with open('.spotify_refresh_token.secret', 'wb') as f:
                pickle.dump(data, f)

            self.__client = spotipy.Spotify(auth=self.__access_token)


        def isLogined(self):

            if self.__getRefreshToken():
                self.__client = spotipy.Spotify(auth=self.__access_token)
                return True
            
            else:
                return False



        def __getAccessToken(self):
            #start server
            #handling the code
            webbrowser.open_new(self.__urlCode)
            
            self.__code = Spotify.Server.code

            self.__body_params = {
                'grant_type': self.__grant_type,
                'code': self.__code,
                'redirect_uri': self.__redirect,
                }

            #getting access_token by POST request to Spotify API
            response = requests.post(
                self.__url,
                data=self.__body_params,
                auth=(
                    self.__client_id,
                    self.__client_secret
                )
            ).json()

            self.__access_token = response['access_token']
            self.__refresh_token = response['refresh_token']

            data = {'refresh_token' : self.__refresh_token}

            with open('.spotify_refresh_token.secret', 'wb') as f:
                pickle.dump(data, f)


        def __getAccessTokenByRefreshToken(self, refresh_token):
            response = requests.post('https://accounts.spotify.com/api/token?',
                                     {
                                        'grant_type': 'refresh_token',
                                        'refresh_token': str(refresh_token),
                                        'client_id': self.__client_id,
                                        'client_secret': self.__client_secret
                                    }
                                ).json()
            self.__access_token = response['access_token']

        def __getRefreshToken(self):

            try:

                with open('.spotify_refresh_token.secret', 'rb') as f:
                    data = pickle.load(f)
                self.__getAccessTokenByRefreshToken(data['refresh_token'])

                return True

            except:

                if not self.server:
                    self.__getAccessToken()

                else:
                    return False

        def __getData(self):
            try:

                with open('.spotify_data.secret', 'rb') as f:
                    data = pickle.load(f)

                self.__client_id = data['client_id']
                self.__client_secret = data['client_secret']

            except:
                print('''
                A new version is available on GitHub.\n
                Download: https://github.com/artyshko/smd
                ''')
                sys.exit()

        def check(self):

            try:
                self.__client.me()
                return True
            
            except:
                return False


        def getPlaylistTracks(self, playlist_uri):

            total_tracks = self.__client.user_playlist(
                user=self.__client.current_user()['id'],
                playlist_id=playlist_uri
            )['tracks']['total']

            steps = int(total_tracks)/100
            steps = int(steps) + 1 if int(steps) - steps < 0 else int(steps)

            tracks = []

            for i in range(steps):

                playlist = self.__client.user_playlist_tracks(
                    user=self.__client.current_user()['id'],
                    playlist_id=playlist_uri,
                    offset = i*100
                )

                for j, item in enumerate(playlist['items']):
                    data = item['track']
                    tracks.append({
                        'uri' : str(data['uri'].split(':')[-1]),
                        'name' : data['name'],
                        'artist' : [ artist['name'] for artist in data['artists']],
                        'album' : data['album']['name'],
                        'image' : data['album']['images'][0]['url'],
                        'duration_ms':data['duration_ms']
                    })

            return tracks

        def getTopArtists(self):

            user_top_artists = self.__client.current_user_top_artists(
                limit=50,
                offset=0,
                time_range='medium_term'
            )['items']


            artists = [
                {
                    'spotify':artist['external_urls']['spotify'],
                    'uri':artist['uri'],
                    'id':artist['id'],
                    'name':artist['name'],
                    'image':artist['images'][0]['url'],
                    'image_big':artist['images'][0]['url'],
                    'popularity':artist['popularity'],
                    'followers':artist['followers']['total'],
                    'genres':artist['genres']
                }

                for artist in user_top_artists 

            ]

            shuffle(artists)
            return artists[:20]

        def getUserTracksOld(self):

            user_top_tracks = self.__client.current_user_saved_tracks(
                limit=50,
                offset=0,
            )['items']


            return [

                {
                    'trc_name':track['track']['name'],
                    'trc_uri':track['track']['uri'],
                    'trc_spotify':track['track']['external_urls']['spotify'],
                    'trc_id':track['track']['id'],
                    'alb_name':track['track']['album']['name'],
                    'alb_uri':track['track']['album']['uri'],
                    'alb_spotify':track['track']['album']['external_urls']['spotify'],
                    'alb_id':track['track']['album']['id'],
                    'alb_image':track['track']['album']['images'][-1]['url'],
                    'art_name':track['track']['artists'][0]['name'],
                    'art_uri':track['track']['artists'][0]['uri'],
                    'art_spotify':track['track']['artists'][0]['external_urls']['spotify'],
                    'art_id':track['track']['artists'][0]['id']
                }

                for track in user_top_tracks 

            ]
        
        def getUserTracks(self):

            it, data = 0, []

            while it <= 500:

                try:
                    
                    user_top_tracks = self.__client.current_user_saved_tracks(
                        limit=50,
                        offset=it,
                    )['items']

                    data.extend([

                        {
                            'trc_name':track['track']['name'],
                            'trc_uri':track['track']['uri'],
                            'trc_spotify':track['track']['external_urls']['spotify'],
                            'trc_id':track['track']['id'],
                            'alb_name':track['track']['album']['name'],
                            'alb_uri':track['track']['album']['uri'],
                            'alb_spotify':track['track']['album']['external_urls']['spotify'],
                            'alb_id':track['track']['album']['id'],
                            'alb_image':track['track']['album']['images'][-1]['url'],
                            'art_name':track['track']['artists'][0]['name'],
                            'art_uri':track['track']['artists'][0]['uri'],
                            'art_spotify':track['track']['artists'][0]['external_urls']['spotify'],
                            'art_id':track['track']['artists'][0]['id']
                        }

                        for track in user_top_tracks 

                    ])

                except:
                    pass

                it+= 50

            return data

        def getTopTracks(self):

            user_top_tracks = self.__client.current_user_top_tracks(
                limit=10,
                offset=0,
                time_range='medium_term'
            )['items']

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'trc_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][-1]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in user_top_tracks 

            ]

        def getUserSavedAlbumPrev(self):

            user_saved_albums = self.__client.current_user_saved_albums(
                limit=20,
                offset=0,
            )['items']

            return [

                {
                    'alb_name':album['album']['name'],
                    'alb_uri':album['album']['uri'],
                    'alb_spotify':album['album']['external_urls']['spotify'],
                    'alb_id':album['album']['id'],
                    'alb_image':album['album']['images'][0]['url'],
                    'art_name':album['album']['artists'][0]['name'],
                    'art_id':album['album']['artists'][0]['id'],
                    'count':len(self.getAlbumsTracks(album['album']['id']))
                }

                for album in user_saved_albums
            ]
             
        def getUserArtistsPrev(self):

            user_top_artists = self.__client.current_user_followed_artists(
                limit=50
            )
            
            artists = []

            for artist in user_top_artists['artists']['items']:

                followers = humanize.intword(artist['followers']['total'])
                followers_comma = humanize.intcomma(artist['followers']['total'])

                if str(followers).isdigit():

                    followers = followers_comma

                try:

                    data = {
                        'spotify':artist['external_urls']['spotify'],
                        'uri':artist['uri'],
                        'id':artist['id'],
                        'name':artist['name'],
                        'image':artist['images'][0]['url'],
                        'popularity':artist['popularity'],
                        'followers':artist['followers']['total'],
                        'followers_display':followers,
                        'followers_comma':followers_comma,
                        'genres':artist['genres']
                    }

                except:

                    data = {
                        'spotify':artist['external_urls']['spotify'],
                        'uri':artist['uri'],
                        'id':artist['id'],
                        'name':artist['name'],
                        'image':self.__image,
                        'popularity':artist['popularity'],
                        'followers':artist['followers']['total'],
                        'followers_display':followers,
                        'followers_comma':followers_comma,
                        'genres':artist['genres']
                    }


                artists.append(data) 

            shuffle(artists)
            return artists[:20]
        
        def getUserPlaylistPrev(self):

            user_playlists = self.__client.current_user_playlists(
                limit=50,
                offset=0
            )
            try: 
                playlists = [ 

                    {
                        'spotify':playlist['external_urls']['spotify'],
                        'uri':playlist['uri'],
                        'id':playlist['id'],
                        'name':playlist['name'],
                        'owner':playlist['owner']['display_name'],
                        'owner_id':playlist['owner']['id'],
                        'image':playlist['images'][0]['url'],
                        'tracks_count':playlist['tracks']['total'],
                    }

                    for playlist in user_playlists['items']
                ]
            except:

                playlists=[]

            shuffle(playlists)
            return playlists[:20]
        
        def getPlaylist(self, id, uri):

            playlist = self.__client.user_playlist(
                user=id,
                playlist_id=uri
            )
            

            try:

                return {
                        'description':playlist['description'],
                        'uri':playlist['uri'],
                        'public':playlist['public'],
                        'followers':playlist['followers']['total'],
                        'id':playlist['id'],
                        'name':playlist['name'],
                        'owner':playlist['owner']['display_name'],
                        'owner_id':playlist['owner']['id'],
                        'image':playlist['images'][0]['url'],
                        'tracks_count':playlist['tracks']['total'],
                        'tracks':[
                            {
                                'trc_name':track['track']['name'],
                                'trc_uri':track['track']['uri'],
                                'trc_spotify':track['track']['external_urls']['spotify'],
                                'trc_id':track['track']['id'],
                                'alb_name':track['track']['album']['name'],
                                'alb_uri':track['track']['album']['uri'],
                                'alb_spotify':track['track']['album']['external_urls']['spotify'],
                                'alb_id':track['track']['album']['id'],
                                'alb_image':track['track']['album']['images'][-1]['url'],
                                'art_name':track['track']['artists'][0]['name'],
                                'art_uri':track['track']['artists'][0]['uri'],
                                'art_spotify':track['track']['artists'][0]['external_urls']['spotify'],
                                'art_id':track['track']['artists'][0]['id']
                            }
                        for track in playlist['tracks']['items']
                        ]
                    }
                
            except:

                return {}


        def getNewReleases(self):

            new_releases = self.__client.new_releases(
                limit=50,
                offset=0
            )

            return [ 

                {
                    'alb_name':album['name'],
                    'alb_artist':album['artists'][0]['name'],
                    'alb_uri':album['uri'],
                    'alb_spotify':album['external_urls']['spotify'],
                    'alb_id':album['id'],
                    'alb_image':album['images'][0]['url']
                }

                for album in new_releases['albums']['items']
            ]
            #recommendation_genre_seeds()
        
        def getUserFeaturedPlaylistPrev(self):

            user_playlists = self.__client.featured_playlists(
                limit=50,
                offset=0
            )

            return [ 

                {
                    'spotify':playlist['external_urls']['spotify'],
                    'uri':playlist['uri'],
                    'id':playlist['id'],
                    'name':playlist['name'],
                    'owner':playlist['owner']['display_name'],
                    'owner_id':playlist['owner']['id'],
                    'image':playlist['images'][0]['url'],
                    'tracks_count':playlist['tracks']['total'],
                }

                for playlist in user_playlists['playlists']['items']
            ]

        def getUserRecommendationGenreSeeds(self):

            return self.__client.recommendation_genre_seeds()

        def getUserRecommendationArtists(self):

            artists = self.getUserArtistsPrev()

            uris = [ uri['id'] for uri in artists]
            

            user_genres = self.__client.recommendations(
                seed_artists=uris[:5],
                limit=50
            )

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'tra_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][0]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in user_genres['tracks'] 

            ]
        
        def getUserRecommendationTopArtists(self):
            
            artists = self.getTopArtists()

            uris = [ uri['id'] for uri in artists]
            

            user_genres = self.__client.recommendations(
                seed_artists=uris[:5],
                limit=20
            )

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'tra_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][0]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in user_genres['tracks'] 

            ]

        def getUserRecommendationTopTracks(self):
            
            artists = self.getTopTracks()

            uris = [ uri['trc_id'] for uri in artists]
            

            user_genres = self.__client.recommendations(
                seed_tracks=uris[:5],
                limit=20
            )

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'tra_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][0]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in user_genres['tracks'] 

            ]

        def getUserRecommendationSavedTracks(self):
            
            artists = self.getUserTracks()

            uris = [ uri['trc_id'] for uri in artists]
            

            user_genres = self.__client.recommendations(
                seed_tracks=uris[:5],
                limit=20
            )

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'tra_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][0]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in user_genres['tracks'] 

            ]

        def getAlbumsTracks(self, id=None):

            tracks = self.__client.album_tracks(
                album_id=id,
                limit=50
            )['items']

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'trc_id':track['id'],
                    'trc_preview':track['preview_url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in tracks 

            ]
        
        def getAlbumCopyright(self, id=None):

            album = self.__client.album(
                album_id =id
            )

            return album['copyrights'][0]['text']

        def getArtistsInfo(self, id=None):

            artist = self.__client.artist(
                artist_id =id
            )

            followers = humanize.intword(artist['followers']['total'])
            followers_comma = humanize.intcomma(artist['followers']['total'])

            if str(followers).isdigit():

                followers = followers_comma

            return {
                'spotify':artist['external_urls']['spotify'],
                'uri':artist['uri'],
                'id':artist['id'],
                'name':artist['name'],
                'image':artist['images'][0]['url'],
                'popularity':artist['popularity'],
                'followers':artist['followers']['total'],
                'followers_display':followers,
                'followers_comma':followers_comma,
                'genres':artist['genres']
            }
        
        def getArtistsTopTracks(self, id=None):

            tracks = self.__client.artist_top_tracks(
                artist_id =id
            )

            return [
                {
                    'trc_name':track['name'],
                    'trc_uri':track['uri'],
                    'trc_spotify':track['external_urls']['spotify'],
                    'trc_id':track['id'],
                    'alb_name':track['album']['name'],
                    'alb_uri':track['album']['uri'],
                    'alb_spotify':track['album']['external_urls']['spotify'],
                    'alb_id':track['album']['id'],
                    'alb_image':track['album']['images'][-1]['url'],
                    'art_name':track['artists'][0]['name'],
                    'art_uri':track['artists'][0]['uri'],
                    'art_spotify':track['artists'][0]['external_urls']['spotify'],
                    'art_id':track['artists'][0]['id']
                }

                for track in tracks['tracks'] 

            ]

        def getArtistsAlbums(self, id=None):

            albums = self.__client.artist_albums(
                artist_id =id,
                limit=50,
                album_type=['album','single','compilation']
            )['items']

            data = [

                {
                    'alb_name':album['name'],
                    'alb_uri':album['uri'],
                    'alb_spotify':album['external_urls']['spotify'],
                    'alb_id':album['id'],
                    'alb_image':album['images'][0]['url'],
                    'alb_r_d':album['release_date']
                }

                for album in albums
            ]

            clear_data = []
            for item in data:

                state = True

                for cleared in clear_data:

                    if cleared['alb_name'] == item['alb_name']:

                        state = False
                
                if state:
                    clear_data.append(item)

            
            return data

        def getArtistsAlbumsSortedByDate(self, id=None):

            albums = self.__client.artist_albums(
                artist_id =id,
                limit=50,
                album_type=['album','single']
            )['items']

            data = [

                {
                    'alb_name':album['name'],
                    'alb_uri':album['uri'],
                    'alb_spotify':album['external_urls']['spotify'],
                    'alb_id':album['id'],
                    'alb_image':album['images'][0]['url'],
                    'alb_r_d':album['release_date'],
                    'total_tracks':album['total_tracks'],
                    'copyrights':self.getAlbumCopyright(album['id']),
                    'year':int(str(album['release_date']).split('-')[0]),
                    'tracks':self.getAlbumsTracks(album['id'])
                }

                for album in albums
            ]

            clear_data = []
            for item in data:

                state = True

                for cleared in clear_data:

                    if cleared['alb_name'] == item['alb_name']:

                        state = False
                
                if state:
                    clear_data.append(item)

            
            return clear_data

        def getArtistsAppearsOn(self, id=None):

            albums = self.__client.artist_albums(
                artist_id =id,
                limit=50,
                album_type=['appears_on','compilation']
            )['items']

            try:
                data = [

                    {
                        'alb_name':album['name'],
                        'alb_uri':album['uri'],
                        'alb_spotify':album['external_urls']['spotify'],
                        'alb_id':album['id'],
                        'alb_image':album['images'][0]['url']
                    }

                    for album in albums
                ]

            except:
                data = []

            return data

        def getArtistsRelatedArtists(self, id=None):

            artists = self.__client.artist_related_artists(
                artist_id =id
            )['artists']
            try:
                data = [
                    {
                        'spotify':artist['external_urls']['spotify'],
                        'uri':artist['uri'],
                        'id':artist['id'],
                        'name':artist['name'],
                        'image':artist['images'][0]['url'],
                        'popularity':artist['popularity'],
                        'followers':artist['followers']['total'],
                        'genres':artist['genres']
                    }

                    for artist in artists

                ]

                shuffle(data)
                return data
            except:
                return []
        
        def getSongInfo(self,id=None):
            
            track = self.__client.track(
                track_id =id
            )

            return {
                'trc_name':track['name'],
                'trc_number':track['track_number'],
                'trc_explicit':track['explicit'],
                'trc_popularity':track['popularity'],
                'trc_duration_ms':track['duration_ms'],
                'trc_duration_display':str(datetime.datetime.fromtimestamp(track['duration_ms']/1000.0).time())[:5],
                'trc_preview_url':track['preview_url'],
                'trc_uri':track['uri'],
                'trc_spotify':track['external_urls']['spotify'],
                'trc_id':track['id'],
                'alb_name':track['album']['name'],
                'alb_uri':track['album']['uri'],
                'alb_spotify':track['album']['external_urls']['spotify'],
                'alb_id':track['album']['id'],
                'alb_image':track['album']['images'][0]['url'],
                'art_name':track['artists'][0]['name'],
                'art_uri':track['artists'][0]['uri'],
                'art_spotify':track['artists'][0]['external_urls']['spotify'],
                'art_id':track['artists'][0]['id']
            }
        
        def getAlbumInfo(self,id=None):
            
            album = self.__client.album(
                album_id =id
            )

            return  [{
                    'alb_name':album['name'],
                    'alb_uri':album['uri'],
                    'alb_spotify':album['external_urls']['spotify'],
                    'alb_id':album['id'],
                    'alb_image':album['images'][0]['url'],
                    'alb_r_d':album['release_date'],
                    'alb_genres':album['genres'],
                    'alb_popularity':album['popularity'],
                    'total_tracks':album['total_tracks'],
                    'copyrights':self.getAlbumCopyright(album['id']),
                    'year':int(str(album['release_date']).split('-')[0]),
                    'art_name':album['artists'][0]['name'],
                    'art_uri':album['artists'][0]['uri'],
                    'art_spotify':album['artists'][0]['external_urls']['spotify'],
                    'art_id':album['artists'][0]['id'],
                    'tracks':self.getAlbumsTracks(album['id'])
                }]

        def getCategories(self):  
            categories = self.__client.categories(
                limit=50,
                offset=0
            )['categories']

                
            return [ 

                {
                    'spotify':category['href'],
                    'id':category['id'],
                    'name':category['name'],
                    'image':category['icons'][0]['url'],
                }

                for category in categories['items']
            ]

            #category_playlists
       
        def getCategoryPlaylists(self, uri):

            playlists = self.__client.category_playlists(
                limit=50,
                category_id=uri
            )

            

            return [{
                    'spotify':playlist['external_urls']['spotify'],
                    'uri':playlist['uri'],
                    'id':playlist['id'],
                    'name':playlist['name'],
                    'owner':playlist['owner']['display_name'],
                    'owner_id':playlist['owner']['id'],
                    'image':playlist['images'][0]['url'],
                    'tracks_count':playlist['tracks']['total']
                } for playlist in playlists['playlists']['items']]

        #current_user_recently_played

        def getRecentlyPlayed(self):
            try:
                data = self.__client.current_user_recently_played(
                    limit=50
                )['items']


                return [

                    {
                        'trc_name':track['track']['name'],
                        'trc_uri':track['track']['uri'],
                        'trc_spotify':track['track']['external_urls']['spotify'],
                        'trc_id':track['track']['id'],
                        'alb_name':track['track']['album']['name'],
                        'alb_uri':track['track']['album']['uri'],
                        'alb_spotify':track['track']['album']['external_urls']['spotify'],
                        'alb_id':track['track']['album']['id'],
                        'alb_image':track['track']['album']['images'][0]['url'],
                        'art_name':track['track']['artists'][0]['name'],
                        'art_uri':track['track']['artists'][0]['uri'],
                        'art_spotify':track['track']['artists'][0]['external_urls']['spotify'],
                        'art_id':track['track']['artists'][0]['id']
                    }

                    for track in data 

                ]
            except:

                return []

        def search(self, query=None):

            data = self.__client.search(
                limit=7,
                q=query,
                type='track'
            )

            try:

                tracks = [

                    {
                        'trc_name':track['name'],
                        'trc_uri':track['uri'],
                        'trc_spotify':track['external_urls']['spotify'],
                        'trc_id':track['id'],
                        'alb_name':track['album']['name'],
                        'alb_uri':track['album']['uri'],
                        'alb_spotify':track['album']['external_urls']['spotify'],
                        'alb_id':track['album']['id'],
                        'alb_image':track['album']['images'][-1]['url'],
                        'art_name':track['artists'][0]['name'],
                        'art_uri':track['artists'][0]['uri'],
                        'art_spotify':track['artists'][0]['external_urls']['spotify'],
                        'art_id':track['artists'][0]['id']
                    }

                    for track in data['tracks']['items'] 

                ]

            except:
                tracks = []

            data = self.__client.search(
                limit=10,
                q=query,
                type='album'
            )
            try:
                albums = [

                    {
                        'alb_name':album['name'],
                        'alb_uri':album['uri'],
                        'alb_spotify':album['external_urls']['spotify'],
                        'alb_id':album['id'],
                        'alb_image':album['images'][0]['url'],
                        'art_name':album['artists'][0]['name'],
                        'art_id':album['artists'][0]['id'],
                        'count':len(self.getAlbumsTracks(album['id']))
                    }

                    for album in data['albums']['items']
                ]
            
            except:
                albums = []

            data = self.__client.search(
                limit=10,
                q=query,
                type='artist'
            )
            
            artists = []
            print(len(data['artists']['items']))

            for artist in data['artists']['items']:

                try:
                    art = {
                            'spotify':artist['external_urls']['spotify'],
                            'uri':artist['uri'],
                            'id':artist['id'],
                            'name':artist['name'],
                            'image':artist['images'][0]['url']
                    }

                    print(art,'\n')
                    
                    artists.append(art)
                except:
                    pass

            data = self.__client.search(
                limit=10,
                q=query,
                type='playlist'
            )

            try:
                playlists = [ 

                    {
                        'spotify':playlist['external_urls']['spotify'],
                        'uri':playlist['uri'],
                        'id':playlist['id'],
                        'name':playlist['name'],
                        'owner':playlist['owner']['display_name'],
                        'owner_id':playlist['owner']['id'],
                        'image':playlist['images'][0]['url'],
                        'tracks_count':playlist['tracks']['total'],
                    }

                    for playlist in data['playlists']['items']
                ]

            except:
                playlists = []

            return {
                'tracks':tracks,
                'albums':albums,
                'artists':artists,
                'playlists':playlists
            }

            


    def __init__(self):

        '''
       Init function
       Creating spotify object with access_token
       :return: None
       '''

        self.__url = 'https://accounts.spotify.com/api/token'
        self.__grant_type = 'client_credentials'
        self.__body_params = {
            'grant_type': self.__grant_type
            }

        self.__getData()
        self.__getAccessToken()

        #initialization of spotify client
        self.client = spotipy.Spotify(self.__access_token)
        #sys.exit()


    def __getData(self):
        try:

            with open('.spotify_data.secret', 'rb') as f:
                data = pickle.load(f)

            self.__client_id = data['client_id']
            self.__client_secret = data['client_secret']

        except:
            print('''
            A new version is available on GitHub.\n
            Download: https://github.com/artyshko/smd
            ''')
            sys.exit()


    def __getAccessToken(self):
        #getting access_token by POST request to Spotify API
        response = requests.post(
            self.__url,
            data=self.__body_params,
            auth=(
                self.__client_id,
                self.__client_secret
            )
        ).json()

        self.__access_token = response['access_token']


    def getSongInfo(self, uri):

        data = self.client.track(uri)

        return {
            'uri' : str(uri.split(':')[-1]),
            'name' : data['name'],
            'artist' : [ artist['name'] for artist in data['artists']],
            'album' : data['album']['name'],
            'image' : data['album']['images'][0]['url'],
            'duration_ms' : data['duration_ms']
        }


    def search(self, query):

        result = self.client.search(q=query, type='track', limit=1)
        try:
            data = result['tracks']['items'][0]

            return ({
                'uri' : str(data['uri'].split(':')[-1]),
                'name' : data['name'],
                'artist' : [ artist['name'] for artist in data['artists']],
                'album' : data['album']['name'],
                'image' : data['album']['images'][0]['url'],
                'duration_ms':data['duration_ms']
            })

        except:
            return False


    def getDuration(self, uri):

        data = self.client.track(uri)
        return data['duration_ms']


    def getAlbum(self, uri):
        try:

            album = self.client.album(uri)

            copyright = None

            try:copyright = album['copyrights'][0]['text']
            except:pass

            alb = {
                'name':album['name'],
                'artist':album['artists'][0]['name'],
                'copyright':copyright,
                'image':album['images'][0]['url'],
            }

            tracks = []

            for data in album['tracks']['items']:
                tracks.append({
                    'uri' : str(data['uri'].split(':')[-1]),
                    'name' : data['name'],
                    'artist' : [ artist['name'] for artist in data['artists']],
                    'album' : alb['name'],
                    'image' : alb['image'],
                    'preview_url' : data['preview_url'],
                    'duration_ms' : data['duration_ms']
                })

            alb.setdefault(
                'tracks', tracks
            )

            return alb

        except: return None

if __name__ == '__main__':
    
    u = Spotify.User()