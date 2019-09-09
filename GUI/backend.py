from flask import Flask, render_template, request, redirect, url_for
from random import shuffle
import json
import spotify
import lastfm
import genius
import webbrowser

import subprocess, os, sys
from os.path import expanduser


app = Flask(__name__)
user = spotify.Spotify.User(server=True)
lastfm = lastfm.LastFM()


@app.route("/home", methods=["GET"])
def index():
    
    sp_user_t_a = user.getTopArtists()
    sp_user_s_alb = user.getNewReleases()
    sp_user_t_t = user.getTopTracks()
    sp_user_s_art = user.getUserArtistsPrev()
    sp_user_s_pls = user.getUserPlaylistPrev()
    sp_user_f_pls = user.getUserFeaturedPlaylistPrev()

    shuffle(sp_user_t_a)
    shuffle(sp_user_s_alb)
    shuffle(sp_user_s_art)
    shuffle(sp_user_s_pls)
    shuffle(sp_user_f_pls)

    return render_template(
        'home.html', 
        user_top_artists=sp_user_t_a,
        user_saved_albums=sp_user_s_alb,
        user_top_tracks=sp_user_t_t,
        user_saved_artists=sp_user_s_art,
        user_saved_playlists=sp_user_s_pls,
        user_featured_playlists=sp_user_f_pls
    )

@app.route("/artist/<uri>", methods=["GET"])
def artist(uri):

    sp_artist_info = user.getArtistsInfo(uri)
    sp_artist_t_t = user.getArtistsTopTracks(uri)
    sp_artist_alb = user.getArtistsAlbums(uri)
    sp_artist_r_a = user.getArtistsRelatedArtists(uri)
    sp_artist_a_o = user.getArtistsAppearsOn(uri)
    sp_artist_alb_full = user.getArtistsAlbumsSortedByDate(uri)

    lf_artist_info = lastfm.getArtistsInfo(sp_artist_info['name'])

    #creating tags
    name = str(sp_artist_info['name']).replace(' ','')

    smd_artists_tags = [name]

    return render_template(
        'artist.html',
        artists_info=sp_artist_info,
        artists_top_tracks=sp_artist_t_t,
        artists_albums=sp_artist_alb,
        artists_related=sp_artist_r_a,
        artists_appears_on=sp_artist_a_o,
        artists_albums_full = sp_artist_alb_full,
        artists_info_lf = lf_artist_info,
        artists_tags = smd_artists_tags
    )

@app.route("/artists", methods=["GET"])
def artists():

    sp_user_s_art = user.getUserArtistsPrev()

    return render_template(
        'artists.html',
        user_saved_artists=sp_user_s_art
    )

@app.route("/albums", methods=["GET"])
def albums():
    
    sp_user_alb = user.getUserSavedAlbumPrev()

    return render_template(
        'albums.html',
        user_saved_albums=sp_user_alb
    )

@app.route("/playlists", methods=["GET"])
def playlists():
    
    sp_user_s_art = user.getUserPlaylistPrev()

    return render_template(
        'playlists.html',
        user_saved_albums=sp_user_s_art
    )

@app.route("/category", methods=["GET"])
def category():

    uri = request.args.get('uri', None) # use default value repalce 'None'
    name = request.args.get('name', None)
    image = request.args.get('image', None)

    
    sp_user_s_art = user.getCategoryPlaylists(uri)

    return render_template(
        'category.html',
        user_saved_albums=sp_user_s_art,
        category_image=image,
        category_name=name
    )

@app.route("/categories", methods=["GET"])
def categories():
    
    sp_user_s_art = user.getCategories()

    return render_template(
        'categories.html',
        user_saved_albums=sp_user_s_art
    )

@app.route("/saved", methods=["GET"])
def saved():
    
    sp_user_s_art = user.getUserTracks()

    return render_template(
        'saved.html',
        artists_top_tracks=sp_user_s_art
    )

@app.route("/playlists/<uri>:<us>", methods=["GET"])
def playlist(uri,us):

    playlist = user.getPlaylist(id=us, uri=uri)

    return render_template(
        'playlist.html',
        info=playlist,
        artists_top_tracks=playlist['tracks']
)

@app.route("/global_top", methods=["GET"])
def global_top():

    playlist = user.getPlaylist(id='spotify', uri='37i9dQZEVXbMDoHDwVN2tF')

    return render_template(
        'playlist.html',
        info=playlist,
        artists_top_tracks=playlist['tracks']
)

@app.route("/last", methods=["GET"])
def last():

    last = user.getRecentlyPlayed()

    return render_template(
        'last_played.html',
        artists_top_tracks=last
)

@app.route("/search/<q>", methods=["GET"])
def search(q):

    query = ' '.join(str(q).split('+'))

    results = user.search(query)

    tracks_res = results['tracks']
    albums_res = results['albums']
    artists_res = results['artists']
    playlists_res = results['playlists']


    return render_template(
        'search.html',
        q=query,
        tracks=tracks_res,
        albums=albums_res,
        artists=artists_res,
        playlists=playlists_res
)

@app.route("/song/<uri>", methods=['GET'])
def song(uri):

    sp_song_data = user.getSongInfo(uri)
    sp_artist_alb = user.getArtistsAlbums(sp_song_data['art_id'])
    sp_artist_r_a = user.getArtistsRelatedArtists(sp_song_data['art_id'])
    sp_artist_alb_full = user.getAlbumInfo(sp_song_data['alb_id'])

    gn_song_lyrics = str(genius.getLyrics(
        artist=sp_song_data['art_name'],
        song=sp_song_data['trc_name']
    )).split('\n')
    

    return render_template(
        'song.html',
        info = sp_song_data,
        artists_albums=sp_artist_alb,
        artists_related=sp_artist_r_a,
        artists_albums_full = sp_artist_alb_full,
        lyrics=gn_song_lyrics
    )

@app.route("/album/<uri>", methods=['GET'])
def album(uri):

    sp_album_data = user.getAlbumInfo(uri)[0]
    sp_artist_alb = user.getArtistsAlbums(sp_album_data['art_id'])
    sp_artist_r_a = user.getArtistsRelatedArtists(sp_album_data['art_id'])


    return render_template(
        'album.html',
        info = sp_album_data,
        artists_albums=sp_artist_alb,
        artists_related=sp_artist_r_a
    )
@app.route("/new_releases", methods=['GET'])
def new_releases():

    rel = user.getNewReleases()

    return render_template(
        'new_releases.html',
        new=rel
    )

@app.route("/for_you", methods=['GET'])
def for_you():

    rel = user.getNewReleases()
    sp_user_f_pls = user.getUserFeaturedPlaylistPrev()
    recom = user.getUserRecommendationArtists()
    recom_t_a = user.getUserRecommendationTopArtists()
    recom_t_t = user.getUserRecommendationTopTracks()
    recom_t_l = user.getUserRecommendationSavedTracks()

    return render_template(
        'for_you.html',
        new=rel,
        rec=recom,
        rec_t_a=recom_t_a,
        rec_t_t=recom_t_t,
        rec_t_l=recom_t_l,
        user_featured_playlists=sp_user_f_pls
    )

@app.route("/other", methods=['GET'])
def other():

    return render_template(
        'other.html'
    )

@app.route("/other_deezer", methods=['GET','POST'])
def other_deezer():

    if request.method == 'POST':


        if request.form['type'] == 'd-track':

            if request.form['data']:

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-ds', request.form['data'],'-p', music])

        elif request.form['type'] == 'd-album':

            if request.form['data']:

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-da', request.form['data'],'-p', music])

        elif request.form['type'] == 'd-pl':
            
            if request.form['data']:

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-dp', request.form['data'],'-p', music])

        else:
            pass
        

        return json.dumps(
            {
                'status': True
            }
        )

    return render_template(
        'other_deezer.html'
    )

@app.route("/other_ytm", methods=['GET','POST'])
def other_ytm():

    if request.method == 'POST':


        if request.form['type'] == 'y-music':

            if request.form['data']:

                data = str(request.form['data']).split('&')[0]

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-ym', data,'-p', music])

        elif request.form['type'] == 'y-video':

            if request.form['data']:

                data = str(request.form['data']).split('&')[0]

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-yv',data,'-p', music])

        else:
            pass
        
        return json.dumps(
            {
                'status': True
            }
        )

    return render_template(
        'other_ytm.html'
    )

@app.route("/other_apple", methods=['GET','POST'])
def other_apple():

    if request.method == 'POST':


        if request.form['type'] == 'a-music':

            if request.form['data']:

                data = str(request.form['data'])

                music = expanduser("~") + '/Music'
                subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-a', data,'-p', music])

        else:
            pass
        
        return json.dumps(
            {
                'status': True
            }
        )

    return render_template(
        'other_apple.html'
    )

@app.route("/downloadSingleSong/<uri>", methods=['GET','POST'])
def downloadSingleSong(uri):

    if request.method == 'POST':

        
        music = expanduser("~") + '/Music'

        subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-ss', f'https://open.spotify.com/track/{uri}','-p', music])
    

        return json.dumps(
            {
                'status': True
            }
        )

@app.route("/downloadAlbum/<uri>", methods=['GET','POST'])
def downloadAlbum(uri):

    if request.method == 'POST':

        music = expanduser("~") + '/Music'

        subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-sa', f'https://open.spotify.com/album/{uri}', '-p', music])

        return json.dumps(
            {
                'status': True
            }
        )

@app.route("/downloadPlaylist/<uri>", methods=['GET','POST'])
def downloadPlaylist(uri):

    if request.method == 'POST':

        music = expanduser("~") + '/Music'

        subprocess.Popen(["python3", f"{os.getcwd()}/main.py", '-sp', f'https://open.spotify.com/playlist/{uri}', '-p', music])

        return json.dumps(
            {
                'status': True
            }
        )

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':


        if user.isLogined():

            return json.dumps(
                {
                    'status': 'http://127.0.0.1:5000/home'
                }
            ) 

        else:
            return json.dumps(
                {
                    'status': user.getURL()
                }
            )
    
    else:

        return render_template(
            'login.html'
        )

@app.route('/linkGitHub', methods=['GET','POST'])
def linkGitHub():

    if request.method == 'POST':

        webbrowser.open_new('https://github.com/artyshko/smd')

        return json.dumps(
                {
                    'status': True
                }
            )


@app.route('/linkTelegram', methods=['GET','POST'])
def linkTelegram():

    if request.method == 'POST':

        webbrowser.open_new('https://t.me/SpotifyMusicDownloaderBot')

        return json.dumps(
                {
                    'status': True
                }
            )

@app.route('/listenOnSpotifySong/<uri>', methods=['GET','POST'])
def listenOnSpotifySong(uri):

    if request.method == 'POST':

        webbrowser.open_new(f'https://open.spotify.com/track/{uri}')

        return json.dumps(
                {
                    'status': True
                }
            )

@app.route('/listenOnSpotifyAlbum/<uri>', methods=['GET','POST'])
def listenOnSpotifyAlbum(uri):

    if request.method == 'POST':

        webbrowser.open_new(f'https://open.spotify.com/album/{uri}')

        return json.dumps(
                {
                    'status': True
                }
            )

@app.route('/listenOnSpotifyArtist/<uri>', methods=['GET','POST'])
def listenOnSpotifyArtist(uri):

    if request.method == 'POST':

        webbrowser.open_new(f'https://open.spotify.com/artist/{uri}')

        return json.dumps(
                {
                    'status': True
                }
            )

@app.route('/listenOnSpotifyPaylist/<uri>', methods=['GET','POST'])
def listenOnSpotifyPlaylist(uri):

    if request.method == 'POST':

        webbrowser.open_new(f'https://open.spotify.com/playlist/{uri}')

        return json.dumps(
                {
                    'status': user.getURL()
                }
            )      
        

@app.route('/logout', methods=['GET','POST'])
def logout():

    os.remove(f'{os.getcwd()}/.spotify_refresh_token.secret')

    return redirect(url_for('shutdown'))


@app.route('/shutdown', methods=['GET','POST'])
def shutdown():

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    return render_template(
            'login.html'
        )


@app.route('/', methods=['GET','POST'])
def getCode():

    code = request.args.get('code')
    user.serverLogin(code)

    return redirect(url_for('index'))

if __name__ ==  "__main__":

    app.run(debug=True, port=5000)