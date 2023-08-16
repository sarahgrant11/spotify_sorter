import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

# Step 3.1: Authentication
def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'

    # Authentication Data
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

# Step 3.2: Get Playlist Tracks (Replace YOUR_PLAYLIST_ID)
def get_playlist_tracks(access_token, playlist_id):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    playlist_response = requests.get(playlist_url, headers=headers)
    return playlist_response.json()['items']

# Step 3.3: Retrieve Audio Features
def get_audio_features(access_token, track_id):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    features_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    features_response = requests.get(features_url, headers=headers)
    return features_response.json()

# Step 3.4: Sort Tracks (e.g., by Danceability)
def sort_tracks_by_feature(tracks, feature):
    return sorted(tracks, key=lambda x: x[feature], reverse=True)

# Main Function
if __name__ == '__main__':
    CLIENT_ID = 'ef345ee78e124e9c949567add88ed000'
    CLIENT_SECRET = '5025d0fd50d2409189fda0ecd7df38ec'
    PLAYLIST_ID = '3a5CjWt7VYgyUoutDnp4Fh?si=6584d206ef514111'

    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    tracks = get_playlist_tracks(token, PLAYLIST_ID)

    # Get audio features for each track
    for track in tracks:
        track_id = track['track']['id']
        track_features = get_audio_features(token, track_id)
        track.update(track_features)

    # Sort by Danceability (replace 'danceability' with any other feature if needed)
    sorted_tracks = sort_tracks_by_feature(tracks, 'danceability')
    for track in sorted_tracks:
        print(track['track']['name'], track['danceability'])

