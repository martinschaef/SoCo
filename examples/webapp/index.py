import time
import hashlib
import os, traceback

import urllib.request
import requests
import simplejson as json

from flask import Flask, render_template, url_for

from soco import SoCo, discover

import settings
import find_player

app = Flask(__name__)

app.config.from_pyfile('settings.py')

sonos = find_player.find_speaker_with_music()

def gen_sig():
    hash_string = "{}{}{}".format(app.config['ROVI_API_KEY'], app.config['ROVI_SHARED_SECRET'], repr(int(time.time()))).encode('utf-8')
    return hashlib.md5(hash_string).hexdigest()

def get_track_image(artist, album, image_uri):
    image = url_for('static', filename='img/blank.jpg')
    # try:
    #     img_path = os.path.join(app.root_path, "static/img/current-album-art.jpg")
    #     urllib.request.urlretrieve(image_uri, img_path)
    #     image = "/static/img/current-album-art.jpg"
    # except:
    #     traceback.print_exc()
    #     print("Failed to parse image from ", image_uri)
    if image_uri is not None:
        image = image_uri

    return image

@app.route("/play")
def play():
    if sonos:
        sonos.play()

    return 'Ok'

@app.route("/pause")
def pause():
    if sonos:
        sonos.pause()

    return 'Ok'

@app.route("/next")
def next():
    if sonos:
        sonos.next()

    return 'Ok'

@app.route("/previous")
def previous():
    if sonos:
        sonos.previous()

    return 'Ok'

def get_track():
    global sonos
    # Check if the current player is still playing music. If not, find another one.
    sonos = find_player.find_speaker_with_music(sonos)    
    track = {'title': '', 'artist': '', 'album': '', 'album_art': '',
            'position': '', 'speaker': ''}
    if sonos:
        track = sonos.get_current_track_info()
        if sonos.player_name:
            track['speaker'] = "Playing on " + sonos.player_name
    return track
    

@app.route("/info-light")
def info_light():
    track = get_track()
    return json.dumps(track)

@app.route("/info")
def info():
    track = get_track()
    track['image'] = get_track_image(track['artist'], track['album'], track['album_art'])

    return json.dumps(track)

@app.route("/")
def index():
    track = get_track()
    track['image'] = get_track_image(track['artist'], track['album'], track['album_art'])

    return render_template('index.html', track=track)

if __name__ == '__main__':
    app.run(debug=True)
