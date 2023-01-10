# pset3.py

import sys, os
import random
sys.path.insert(0, os.path.abspath('..'))

#Spotify imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from functools import partial
#import config file
from melakarta import scale_to_rag
from random import randint, random
from playscale import play_raga
import numpy as np
from flask import Flask, request, render_template, send_file, send_from_directory


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=["GET"])
def hello():
    return render_template("raga.html")

@app.route("/", methods=["POST"])
def get_aro_avaro():
    #spotify oauth flow
    search = request.form['text']
    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    result = sp.search(search, limit=1, type='track')
    track_spotify_uri = result['tracks']['items'][0]['uri']
    track_info = sp.track(track_spotify_uri)
    spotifyurl = track_info['external_urls']['spotify']
    artistlist = track_info['artists']
    songname = track_info['name'].lower()
    artistnames = [elem['name'] for elem in artistlist]
    if len(artistnames) == 1:
        artists = artistnames[0].lower()
    elif len(artistnames) == 2:
        artists = " and ".join(artistnames).lower()
    else:
        artists = "{}, and {}".format(", ".join(artistnames[:-1]),  artistnames[-1]).lower()
    track_analysis = sp.audio_analysis(track_spotify_uri)
    key = track_analysis['track']['key']
    segments = track_analysis['segments']
    scale_t = {}
    scale = {}
    for i in range(12):
        scale_t[i] = 0
        scale[i] = 0
    for elem in range(len(segments)//12, len(segments)//4):
        signal = segments[elem]['pitches']
        for i, elem1 in enumerate(signal):
            if elem1 >= 0.9:
                scale[i] += 1
    for elem in range(3*len(segments)//4, 11*len(segments)//12):
        signal = segments[elem]['pitches']
        for i, elem1 in enumerate(signal):
            if elem1 >= 0.9:
                scale[i] += 1
    for i in scale:
        scale_t[(i - key + 12)%12] = scale[i]
    
    rg = np.argmax([scale_t[1] + scale_t[2], scale_t[1] + scale_t[3], scale_t[1] + scale_t[4], scale_t[2] + scale_t[3], scale_t[2] + scale_t[4], scale_t[3] + scale_t[4]])
    if rg == 0:
        r = 1
        g = 1
    elif rg == 1:
        r = 1
        g = 2
    elif rg == 2:
        r = 1
        g = 3
    elif rg == 3:
        r = 2
        g = 2
    elif rg == 4:
        r = 2
        g = 3
    elif rg == 5:
        r = 3
        g = 3
    
    m = np.argmax([scale_t[5], scale_t[6]]) + 1

    dn = np.argmax([scale_t[8] + scale_t[9], scale_t[8] + scale_t[10], scale_t[8] + scale_t[11], scale_t[9] + scale_t[10], scale_t[9] + scale_t[11], scale_t[10] + scale_t[11]])
    if rg == 0:
        d = 1
        n = 1
    elif rg == 1:
        d = 1
        n = 2
    elif rg == 2:
        d = 1
        n = 3
    elif rg == 3:
        d = 2
        n = 2
    elif rg == 4:
        d = 2
        n = 3
    elif rg == 5:
        d = 3
        n = 3

    arorep = "S R{} G{} M{} P D{} N{} S".format(r, g, m, d, n)
    play_raga(arorep)
    return render_template('answer.html', aro=arorep, song=songname, raga=scale_to_rag[arorep].lower(), artists=artists, url=spotifyurl)

@app.route("/test.wav")
def returnAudioFile():
    return send_from_directory(
    os.path.join(os.getcwd()),
    "test.wav",
    as_attachment=True)

@app.route("/about")
def about():
    return render_template('about.html')

@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store, max-age=0'
    return response