# Standard Library Imports
import base64
import io
import os

# Third party imports
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def playlist(playlist_id):
    playlist_id = playlist_id
    results = sp.playlist(playlist_id)

    ids = {'id': []}
    for item in results['tracks']['items']:
        track = item['track']['id']
        ids['id'].append(track)

    """
    def create_song_meta_list(ids):
        song_meta = {'id': []}
        for song_id in ids:
            song_meta['id'].append(song_id)
    """

    song_meta_df = pd.DataFrame.from_dict(ids)
    # check the song feature
    features = sp.audio_features(ids['id'])
    # change dictionary to dataframe
    features_df = pd.DataFrame.from_dict(features)
    m_feature = features_df[['danceability', 'energy', 'loudness', 'acousticness',
                                 'liveness', 'valence', 'tempo']]

    def scale(mf_df):
        music_feature = mf_df
        # make sure error message isn't there anymore
        pd.options.mode.chained_assignment = None
        min_max_scaler = MinMaxScaler()
        music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])
        return music_feature

    def plot_features(music_feature):
        plt.figure(figsize=(12, 8))
        categories = list(music_feature.columns)  # list of column names
        cat_len = len(categories)  # convert column names into a list
        value = list(music_feature.mean())  # list with average of all features
        value += value[:1]
        angles = [n / float(cat_len) * 2 * np.pi for n in range(cat_len)]
        angles += angles[:1]
        plt.polar(angles, value)
        plt.fill(angles, value, alpha=0.3)
        plt.xticks(angles[:-1], categories, size=15)
        plt.yticks(color='grey', size=15)
        # save image to base64
        my_stringIObytes = io.BytesIO()
        my_stringIObytes.truncate(0)
        plt.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
        plt.close()
        return my_base64_jpgData

    mf_scale = scale(m_feature)
    return plot_features(mf_scale)