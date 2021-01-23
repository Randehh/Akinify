import os
import tweepy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging
import math

import asyncio
from dotenv import load_dotenv

import spotify

load_dotenv()

tweepy_api = None
spotipy_api = None

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print("Tweet received")
		print(status.text)

	def on_error(self, status_code):
		print("Error: " + str(status_code))
		return True

def main():
	print("Starting...")

	if os.getenv('CREATE_TWITTER_API') == "1":
		print("Creating Twitter API")
		tweepy_api = get_tweepy_api()
		streamListener = StreamListener()
		myStream = tweepy.Stream(auth=api.auth, listener=streamListener)
		myStream.filter(track = ["@Akinify"])
	
	if os.getenv('CREATE_SPOTIFY_API') == "1":
		print("Creating Spotify API")
		CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
		CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
		#spotipy_api = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

		scope = "playlist-modify-public"
		spotipy_api = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

		print("Test request for spotify")
		artist_uri = "spotify:artist:4sj7VQUlAl4Bkkxudd5h3E"
		artist_name = "Graham Kartna 2"
		related_artists_set = set()
		search_depth = 1
		spotify.get_related_artists(spotipy_api, artist_uri, search_depth, related_artists_set)
		print(str(len(related_artists_set)) + " ARTISTS")
		
		top_tracks_from_artists = spotify.get_top_tracks_from_artists(spotipy_api, related_artists_set, 10)
		print(str(len(top_tracks_from_artists)) + " TRACKS")

		trimmed_track_set = spotify.get_trimmed_track_set(top_tracks_from_artists, search_depth)
		print(str(len(trimmed_track_set)) + " TRIMMED TRACKS")

		spotify.create_playlist_from_track_uri_set(spotipy_api, trimmed_track_set, "Akinify - " + artist_name, "A playlist based on artist " + artist_name)

def get_tweepy_api():
	CONSUMER_KEY = os.getenv('CONSUMER_KEY')
	CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
	ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
	ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.secure = True
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
	try:
		api.verify_credentials()
		print("API successfully created")
	except Exception as e:
		print("Error creating API")

	return api

if __name__ == "__main__":
	main()