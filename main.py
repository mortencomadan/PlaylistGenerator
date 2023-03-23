import spotify

artist_list = spotify.return_list_of_artists_from_playlist("6hx45zkRiMmhT3zYRzLm2B")
song_list = spotify.get_song_list_from_artist_list(artist_list, 10)
spotify.create_playlist("MetalDays top 10", song_list)