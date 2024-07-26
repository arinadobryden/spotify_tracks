# Spotify Top Artist Tracks Web Service #
## Arina Dobryden F28IR - Final CW 
This project is an online service that allows users to select an artist and a country, to view their top tracks. This is using the Spotify API, which provides a web service to track searches, as well as offering a real-time chat option for the active users. 

## Features
- Fetches top 10 tracks of artist, available in specified country
- Determines user's country based on their IP, if no country is provided
- Stores search history, providing an API endpoint to retrieve the last 20 searches
- Real-time chat functionality for users

## Installation and setup
- Clone the repository
```
git clone https://github.com/yourusername/spotify-top-tracks.git
cd spotify-top-tracks
```
- Create a VE and install dependencies
```
python -m venv venv
`venv\Scripts\activate`
pip install -r requirements.txt
```
- Setup Spotify API Credentials
```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=https://example.org/callback
```
- Run the application


```
python app.py
```
- Open browser and navigate to 'http://localhost:5000'


## Funtional Requirements
1. Implemented in HTML
2. Implemented using the Spotify API in the app.py script.
3. Implemented using the IP-API service in the app.py script.
4. Implemented using the Spotify API in the app.py script.
5. Implemented in the JavaScript and HTML.
6. Implemented in the app.py script with the /searches endpoint. 
7. Implemented using Flask-SocketIO.

## Non-Functional Requirements
1. Implemented using JavaScript for dynamic updates.
2. Implemented using audio preview URLs from the Spotify API.
3. Ensured throughout the project development.
4. User-friendly interface with no need for users to know country codes.
5. Implemented in the API responses.
