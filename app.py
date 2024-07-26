from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_socketio import SocketIO, emit
import requests
import os
import logging

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

SPOTIFY_API_URL = 'https://api.spotify.com/v1'
CLIENT_ID = 'dac80e6b645542e0bcad78ba22b520c3'
CLIENT_SECRET = '5532396c309048ed92da1f76a6503539'
REDIRECT_URI = 'https://example.org/callback'  # Update this to your actual callback URL
    
logging.basicConfig(level=logging.DEBUG)

def get_access_token():
    global access_token
    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    access_token = auth_response.json().get('access_token')
    logging.debug(f"Access token: {access_token}")

get_access_token()
@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/top-tracks', methods=['GET'])
def top_tracks():
    artist_name = request.args.get('artist')
    country = request.args.get('country')

    logging.debug(f"Artist: {artist_name}, Country: {country}")

    if not artist_name:
        logging.error("No artist name provided")
        return redirect(REDIRECT_URI)

    if not country or country.strip() == '':
        # Fetch user's country based on IP (example implementation)
        country_response = requests.get('http://ip-api.com/json')
        country = country_response.json().get('countryCode', 'US')
        logging.debug(f"Detected country: {country}")

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    search_response = requests.get(
        f'{SPOTIFY_API_URL}/search',
        headers=headers,
        params={
            'q': artist_name,
            'type': 'artist',
            'market': country,
            'limit': 1,
        },
    )
    logging.debug(f"Search response: {search_response.json()}")

    if search_response.status_code != 200 or not search_response.json()['artists']['items']:
        logging.error("Artist not found or search failed")
        return redirect(REDIRECT_URI)

    artist_id = search_response.json()['artists']['items'][0]['id']
    logging.debug(f"Artist ID: {artist_id}")

    top_tracks_response = requests.get(
        f'{SPOTIFY_API_URL}/artists/{artist_id}/top-tracks',
        headers=headers,
        params={
            'market': country,
        },
    )
    logging.debug(f"Top tracks response: {top_tracks_response.json()}")

    if top_tracks_response.status_code != 200:
        logging.error("Failed to get top tracks")
        return redirect(REDIRECT_URI)

    tracks = top_tracks_response.json().get('tracks', [])[:10]
    track_list = [{
        'name': track['name'],
        'preview_url': track['preview_url'],
        'album': {
            'images': track['album']['images']
        }
    } for track in tracks]

    if not tracks:
        logging.error("No tracks found")
        return redirect(REDIRECT_URI)

    # Store the search info (example using a list)
    # In production, use a database
    with open('search_log.txt', 'a') as log_file:
        log_file.write(f'{artist_name},{country},{len(tracks)}\n')

    return jsonify(track_list)

@app.route('/searches', methods=['GET'])
def get_searches():
    with open('search_log.txt', 'r') as log_file:
        searches = log_file.readlines()[-20:]
    return jsonify([search.strip().split(',') for search in searches])

@app.route('/failure')
def failure():
    return send_from_directory('', 'failure.html')

@socketio.on('message')
def handle_message(data):
    emit('message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)