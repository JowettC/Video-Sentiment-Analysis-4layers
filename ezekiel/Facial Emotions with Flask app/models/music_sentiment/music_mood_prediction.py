import pickle
import numpy as np 
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET')))

# Get Scaler_fit object to fit one dataset
def get_scaler_fitted():
    df = pd.read_csv("./models/music_sentiment/songs_default.csv")
    df['mood'] = df['mood'].replace(['calm', 'happy','angry','depress'], [1,1,0,0])
    df.drop_duplicates(subset=['name', 'artist', 'mood'], keep='last',inplace=True)
    col_features = df.columns[7:-3]
    scaler = MinMaxScaler()
    scaler_fit = scaler.fit(df[col_features])
    return scaler_fit

# Helper function to get songs details using songs id
def get_songs_features(ids):
    meta = sp.track(ids)
    features = sp.audio_features(ids)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    ids =  meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
            energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name','album','artist','id','release_date','popularity','length','danceability','acousticness','energy','instrumentalness',
                'liveness','valence','loudness','speechiness','tempo','key','time_signature']
    return track,columns

# Get mood of song 
def get_song(artist,track,model):
    # get song details from spotify api
    results = sp.search(q='artist:' + artist + ' track:' + track, type='track')
    song_id = results['tracks']['items'][0]['id']
    song_feature = get_songs_features(song_id)

    # getting X data from song details
    col_features = ['length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
    'liveness', 'valence', 'loudness', 'speechiness', 'tempo']
    song_feature = np.array(song_feature[0][6:-2]).reshape(-1,1).T
    song_feature = pd.DataFrame(song_feature, columns = col_features)

    # scaling single data by using scalar fitted previously  
    scaler_fit = get_scaler_fitted()
    song_feature_scaled = scaler_fit.transform(song_feature)
#     print(song_feature_scaled)

    # predicting mood using trained model of plk
    mood = model.predict(song_feature_scaled)
    mood = 'Positive' if mood == 1 else 'Negative'
    print(f"{track} by {artist} is a {mood} song")
    return mood 

def main():
    model = pickle.load(open('./weihern/LSVC_best.pkl', 'rb'))
    check_list = [('Vampire Weekend','A-Punk'),('Linkin Park','Battle Symphony'),
              ('The Fratellis','Chelsea Dagger'),('Justin Bieber','Peaches'),
              ('MKTO','Classic'),('Pharrell Williams','Happy'),('Ed Sheeran','Photograph'),
              ('Sam Smith','I am not the only one')]
    # print mood for all those songs to check 
    for artist,track in check_list:
        get_song(artist,track,model)

if __name__ == "__main__":
    main()
