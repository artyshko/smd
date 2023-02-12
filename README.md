# Spotify Music Downloader (SMD) Desktop | **<a href="https://t.me/SpotifyMusicDownloaderBot"><b>Telegram</b></a>**
<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/telegram/Data/9.png">

Spotify Music Downloader acts as a third-party platform where the user is able to interact with the GUI, Telegram, or through the command-line to download songs from Spotify, YouTube Music, and Apple Music.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![GitHub repo size in bytes](https://img.shields.io/github/repo-size/artyshko/smd.svg) ![GitHub Release Date](https://img.shields.io/github/release-date/artyshko/smd.svg) ![GitHub issues](https://img.shields.io/github/issues/artyshko/smd.svg) ![Beerpay](https://img.shields.io/beerpay/artyshko/smd.svg) [![Beerpay](https://beerpay.io/artyshko/smd/make-wish.svg?style=flat)](https://beerpay.io/artyshko/smd?focus=wish)

## Table of Content
Below contains information that the user might find helpful to utilize SMD:
* [Update](#update)
  * Holds important information about the current state of SMD
* [Installation](#installation)
  * How to install the dependencies
* [Commands](#commands)
  * The commands to run to download songs
  * Shows commands for different platforms 
* [Images](#images)
  * Shows pictures of the GUI of different platforms
  * Spotify, Telegram, CLI, etc...

## Update

#### NEW DEV VERSION **<a href="https://github.com/artyshko/smd/tree/dev_ea-0"><b>HERE</b></a>** (As the bot is down, you can use this CLI version)
#### The SMD project is temporarily frozen due to having problems with a DMCA.

## Installation

```
git clone https://github.com/artyshko/smd.git
```

#### First you have to install all dependencies
```
pip3 install -r requirements.txt
pip3 install PyQtWebEngine
sudo apt-get install python3-pyqt5.qtwebengine
```

#### Make file executable
```
chmod +x main.py
./main.py
```
#### Or use
```
python3 main.py
```

#### Desktop version (CLI)

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

## Commands
### Desktop version (CLI) commands
| Command | Description |
| --- | --- |
| -h,  --help | Print a help message and exit. |
| -p,  --path | Set another directory. |
| -ss, --spotify-song | Spotify song link or URL. |
| -sa, --spotify-album | Spotify album link or URL. |
| -sp, --spotify-playlist | Spotify playlist URL. |
| -ds, --deezer-song | Deezer playlist link. |
| -da, --deezer-album | Deezer album link. |
| -dp, --deezer-playlist | Deezer playlist link. |
| -ym, --youtube-music | YouTube Music link. |
| -yv, --youtube-video | YouTube Video link. |
| -a,  --apple | Apple Music link. |
| -q,  --query | Search query. |

#### Query mode
Example:
```
./main.py -q "The XX - Intro"
```

#### Choose another directory 
Example:
```
./main.py -q "The XX - Intro" -p ~/Music

./main.py -ss "https://open.spotify.com/track/2QoDAlMnML5haTXvYRS86X" -p ~/Desktop/Music/New
```
#### Spotify 
Song:
```
./main.py -ss "https://open.spotify.com/track/2QoDAlMnML5haTXvYRS86X?si=eMGX4dlwQd-7dyiG6OmUHQ"
```
Album:
```
./main.py -sa "https://open.spotify.com/album/79dL7FLiJFOO0EoehUHQBv?si=lDnHRa2BR_uFUOnUOZPbUQ"
```
Playlist:
```
./main.py -sp "https://open.spotify.com/playlist/37i9dQZF1DXcRXFNfZr7Tp?si=Yd3IJQ9ATWOdFulNa7ax5g"
```

#### Deezer
Song:
```
./main.py -ds "https://www.deezer.com/track/3787855"
```
Album:
```
./main.py -da "https://www.deezer.com/album/1695172"
```
Playlist:
```
./main.py -dp "https://www.deezer.com/playlist/1306931615"
```

#### YouTube Music
Song:
```
./main.py -ym "https://music.youtube.com/watch?v=HnXzzTIFu_U&list=RDAMVMHnXzzTIFu_U"
```

#### YouTube Video
Video:
```
./main.py -yv "https://www.youtube.com/watch?v=JHi-WGFGWek"
```

#### Apple Music
Example:
```
./main.py -a "https://itunes.apple.com/us/album/i-wanna-be-yours/663097964?i=663098065"
```

## Images

### Desktop version GUI

<p align="center">
 
</p>
 <img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/1.png"> 
.
 <img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/2.png">
<p align="center">

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/6.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/7.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/3.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/4.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/5.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/8.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/9.png"></br>

<img align="center" src="https://github.com/artyshko/smd/raw/master/Data/prev/10.png"></br>
 
  <b><h1>Desktop version CLI<h1></b>
</p>
  <img align="center" src="https://github.com/artyshko/smd/raw/master/Data/11.png">
<p align="center">
  <h1>Telegram version</h1>
</p>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/1.png"></br>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/2.png"></br>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/3.png"></br>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/4.png"></br>

<img align="center" src="https://raw.githubusercontent.com/artyshko/smd/master/Data/5.png"></br>



