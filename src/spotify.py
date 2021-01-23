def get_related_artists(spotipy_api, artist_uri, depth, artist_set, current_depth = -1):
    if current_depth == -1:
        current_depth = depth
    
    current_depth = current_depth - 1
    
    result = spotipy_api.artist_related_artists(artist_uri)
    artist_limit = int(100 / (depth - current_depth))
    for artist_result in result["artists"][:artist_limit]:
        related_artist_uri = artist_result["uri"]
        artist_set.add(related_artist_uri)
        if current_depth != 0:
            get_related_artists(spotipy_api, related_artist_uri, depth, artist_set, current_depth=current_depth)

def get_top_tracks_from_artists(spotipy_api, artist_uri_set, song_count):
    track_set = set()
    
    for artist_uri in artist_uri_set:
        result = spotipy_api.artist_top_tracks(artist_uri)
        for track_data in result["tracks"]:
            track_set.add(str(track_data["uri"]))

    return track_set

def get_trimmed_track_set(track_uri_set, search_depth):
    trimmed_set = set()

    base_list_length = 100
    song_count = base_list_length
    for x in range(search_depth):
        base_list_length = base_list_length / 1.5
        song_count = song_count + base_list_length
    
    print("Final list size = " + str(song_count))

    limit = int(song_count)
    if len(track_uri_set) < song_count:
        limit = len(track_uri_set)
    
    for x in range(limit):
        trimmed_set.add(track_uri_set.pop())
    
    return trimmed_set

def create_playlist_from_track_uri_set(spotipy_api, track_uri_set, title, description):
    user = 'akuma-sama'
    playlist_data = spotipy_api.user_playlist_create(user, title, description=description)
    
    track_list = list(track_uri_set)
    while len(track_list) > 0:
        spotipy_api.user_playlist_add_tracks(user, playlist_data["uri"], list(track_list[:100]))
        track_list = track_list[100:]