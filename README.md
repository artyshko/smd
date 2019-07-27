# Spotify Music Downloader (SMD) Desktop | **<a href="https://t.me/SpotifyMusicDownloaderBot"><b>Telegram</b></a>**
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub repo size in bytes](https://img.shields.io/github/repo-size/artyshko/smd.svg) ![GitHub Release Date](https://img.shields.io/github/release-date/artyshko/smd.svg) ![GitHub issues](https://img.shields.io/github/issues/artyshko/smd.svg) ![Beerpay](https://img.shields.io/beerpay/artyshko/smd.svg) [![Beerpay](https://beerpay.io/artyshko/smd/make-wish.svg?style=flat)](https://beerpay.io/artyshko/smd?focus=wish)

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/telegram/Data/9.png"> 

<p align="center">
  <b><h1>Desktop version<h1></b><br>
</p>
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/6.png"> 
<p align="center">
  <h1>Telegram version</h1>
  <h5><a href="https://telegram.me/SpotifyMusicDownloaderBot"><b>@SpotifyMusicDownloaderBot</b></a></h5>
</p>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/1.png">
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/2.png">
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/3.png">
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/4.png">
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/5.png">

## Usage (Desktop version)

```
./main.py [argument][value] - startup with arguments

 Arguments:

        -h,  --help                  Print a help message and exit.
        -p,  --path                  Set another directory.

        -ss, --spotify-song          Spotify song link or URI.
        -sa, --spotify-album         Spotify album link or URI.
        -sp, --spotify-playlist      Spotify playlist URI.

        -ds, --deezer-song           Deezer song link.
        -da, --deezer-album          Deezer album link.
        -dp, --deezer-playlist       Deezer playlist link.

        -ym, --youtube-music         YouTube Music link.
        -yv, --youtube-video         YouTube Video link.

        -a,  --apple                 Apple Music link.
        -q,  --query                 Search query.

```
## Installation

```
git clone https://github.com/artyshko/smd.git
```

### First you need to install all dependencies
```
pip3 install -r requirements.txt
```

### Make file executable
```
chmod +x main.py
./main.py
```
### Or use
```
python3 main.py
```
### How to get song URI

<img align="center" src="https://i.ibb.co/BzM7ZKp/image4.png">

### Example of Spotify URI Code
```
spotify:track:4tmwiN9YU7xMjh2hoqcVuI
```

### Song mode
Example:
```
./main.py -s spotify:track:7ARveOiD31w2Nq0n5FsSf8
```

### Query mode
Example:
```
./main.py -q "The XX - Intro"
```

### YouTube Music mode
Example:
```
./main.py -y "https://music.youtube.com/watch?v=HnXzzTIFu_U&list=RDAMVMHnXzzTIFu_U"
```

### YouTube video mode
Example:
```
./main.py -v "https://www.youtube.com/watch?v=JHi-WGFGWek"
```

### Apple Music mode
Example:
```
./main.py -a "https://itunes.apple.com/us/album/i-wanna-be-yours/663097964?i=663098065"
```

### File mode
#### Create file with songs
<img align="center" src="https://i.ibb.co/qJvgMXB/file.png">

Example:
```
./main.py -f songs.txt
```

### Playlist mode
#### Create playlist and make it secret
<img align="center" src="https://i.ibb.co/kBKtDys/image1.png">

#### Then copy playlist URI
<img align="center" src="https://i.ibb.co/yWHHBDX/image2.png">

Example:
```
./main.py -p spotify:user:spotify:playlist:37i9dQZF1DXcRXFNfZr7Tp
```
