# pset3.py

import sys, os
import random
sys.path.insert(0, os.path.abspath('..'))

#Spotify imports
import spotipy
import spotipy.oauth2 
from functools import partial
#import config file
import config as cfg
from melakarta import scale_to_rag
from random import randint, random
import numpy as np
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return render_template("raga.html")
@app.route("/", methods=["POST"])
def get_aro_avaro():
    print("HIISIIIIIIIIi")
    #spotify oauth flow
    search = request.form['text']
    id = cfg.credentials['id']
    secret = cfg.credentials['secret']
    uri = cfg.credentials['redirect_uri']
    scope = 'user-read-playback-state, user-modify-playback-state, user-read-currently-playing'
    client_credentials_manager = spotipy.SpotifyOAuth(id, secret, uri, scope=scope)
    token_dict = client_credentials_manager.get_access_token()
    token = token_dict['access_token']
    sp = spotipy.Spotify(auth=token)
    result = sp.search(search, limit=1, type='track')
    track_spotify_uri = result['tracks']['items'][0]['uri']
    track_analysis = sp.audio_analysis(track_spotify_uri)
    key = track_analysis['track']['key']
    segments = track_analysis['segments']
    scale_t = {}
    scale = {}
    for i in range(12):
        scale_t[i] = 0
        scale[i] = 0
    for elem in range(len(segments)):
        if segments[elem]['confidence'] >= 0:
            signal = segments[elem]['pitches']
            for i, elem in enumerate(signal):
                if elem >= 0.9:
                    scale[i] += 1
    for i in scale:
        scale_t[(i - key + 12)%12] = scale[i]
    r = np.argmax([scale_t[1], scale_t[2], scale_t[3]]) + 1 
    rind = r
    g = np.argmax([scale_t[k] for k in range(rind+1, 5)]) + 1 + (r-1)
    m = np.argmax([scale_t[5], scale_t[6]]) + 1
    d = np.argmax([scale_t[8], scale_t[9], scale_t[10]]) + 1
    dind = d+7
    n = np.argmax([scale_t[k] for k in range(dind+1, 12)]) + 1 + (d-1)
    arorep = "S R{} G{} M{} P D{} N{} S".format(r, g, m, d, n)
    return render_template('answer.html', song=search, raaga=scale_to_rag[arorep].lower())

