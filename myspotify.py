import audioProvider
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Spotify Client
cid = os.getenv("SPOTIFY_CLIENT_ID")
secret = os.getenv("SPOTIFY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_youtube_link(song_name: str, song_artists: str, song_album: str, duration: str):
    youtube_link = audioProvider.search_and_get_best_match(song_name, song_artists, song_album, duration)
    if youtube_link is None:
        return None
    else:
        return youtube_link

def spotify_fetch(spotify_link):
    # Call Spotify for Metadata
    response = sp.track(spotify_link)
    spotify_name = response["name"]
    spotify_artists = []
    for artist in response["artists"]:
        spotify_artists.append(artist["name"])
    spotify_album = response["album"]["name"]
    duration = round(response["duration_ms"] / 1000, ndigits=3)

    # get youtube link
    return get_youtube_link(song_name=spotify_name, song_artists=spotify_artists, song_album=spotify_album, duration=duration)
