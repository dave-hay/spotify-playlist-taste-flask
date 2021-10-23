import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

load_dotenv()

# Get variables
SCOPE = os.getenv('SCOPE')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Configure Spotipy
conf = SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, scope=SCOPE)
sp = spotipy.Spotify(auth_manager=conf)

results = sp.current_user_top_tracks()

"""ids = []
song_list = []"""

ids = []
song_list = []

for idx, x in enumerate(results['items']):
    song = x['name']
    info = x['id']
    ids.append(info)
    song_list.append(str(idx + 1) + ' - ' + song)

# song_list_df = pd.DataFrame.from_dict(song_list)
features = sp.audio_features(ids)

features_df = pd.DataFrame.from_dict(features)
music_feature = features_df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                             'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']]

# make sure error message isn't there anymore
pd.options.mode.chained_assignment = None
min_max_scaler = MinMaxScaler()
music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])

# plot size
fig = plt.figure(figsize=(12, 8))

# convert column names into a list
categories = list(music_feature.columns)
# number of categories
N = len(categories)

# create a list with the average of all features
value = list(music_feature.mean())

# repeat first value to close the circle
# the plot is a circle, so we need to "complete the loop"
# and append the start value to the end.
value += value[:1]
# calculate angle for each category
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# plot
plt.polar(angles, value)
plt.fill(angles, value, alpha=0.3)

# plt.title('Discovery Weekly Songs Audio Features', size=35)

plt.xticks(angles[:-1], categories, size=15)
plt.yticks(color='grey', size=15)
plt.show()
plt.close()
