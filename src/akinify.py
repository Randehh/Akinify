import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import logging
import math

import asyncio
from dotenv import load_dotenv

import spotify

load_dotenv()

spotipy_api = None

def main():
	print("Verifying arguments...")
	args_length = len(sys.argv)
	if args_length != 3:
		print("ERROR: Argument count " + str((args_length - 1)) + " is not 2! Expected: artist_uri, search_depth")
		return
	
	print("Creating Spotify API...")
	CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
	CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
	scope = "playlist-modify-public"
	spotipy_api = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

	print("Getting artist info...")
	artist_uri = sys.argv[1]
	artist_name = spotify.get_artist_name(spotipy_api, artist_uri)

	print("Getting related artists...")
	related_artists_set = set()
	search_depth = int(sys.argv[2])
	spotify.get_related_artists(spotipy_api, artist_uri, search_depth, related_artists_set)
	print(str(len(related_artists_set)) + " related artists found by search depth of " + str(search_depth))
	
	print("Getting top tracks from artists...")
	top_tracks_from_artists = spotify.get_top_tracks_from_artists(spotipy_api, related_artists_set, 10)
	print(str(len(top_tracks_from_artists)) + " total tracks found")

	print("Selecting tracks...")
	trimmed_track_set = spotify.get_trimmed_track_set(top_tracks_from_artists, search_depth)
	print(str(len(trimmed_track_set)) + " playlist tracks selected")

	print("Creating tracklist...")
	spotify.create_playlist_from_track_uri_set(spotipy_api, trimmed_track_set, "Akinify - " + artist_name, "A playlist based on artist " + artist_name)

	print("Completed! The tracklist should have popped up on your profile.")

if __name__ == "__main__":
	main()