from difflib import SequenceMatcher
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
scope = "playlist-modify-public"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


class Song:
    name = ""
    id = ""


class Band:
    def __init__(self):
        self.name = ""
        self.genres = []
        self.id = ""
        self.found = False
        self.top_5_songs = []


class Artist:
    def __init__(self, id, name):
        self.name = name
        self.id = id


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_top_5(band):
    if not band.id:
        return band

    uri = 'spotify:artist:' + band.id

    results = spotify.artist_top_tracks(uri)
    for track in results['tracks'][:5]:
        song = Song()
        song.id = track["id"]
        song.name = track["name"]
        band.top_5_songs.append(song)

    return band


def find_band_with_song(bands, name_of_first_song):
    for band_obj in bands:
        band = Band()

        band.name = band_obj["name"]
        band.id = band_obj["id"]

        song_name = find_top_5(band).top_5_songs

        for song in song_name:
            if song.name.lower() == name_of_first_song.lower():
                return band_obj


def find_band(name_of_band, find_top_5_songs=False):
    band = Band()
    song_name = ""
    multiple_matches = []

    split = name_of_band.split("|")

    if len(split) > 1:
        band_name = split[0]
        song_name = split[1]
    else:
        band_name = name_of_band

    results = spotify.search(q="artist: " + band_name, type="artist", limit=30)
    items = results["artists"]["items"]

    if len(items):
        best_ratio = 0

        for bands in items:
            ratio = similar(bands["name"].lower(), band_name.lower())

            if ratio > best_ratio:
                best_ratio = ratio
                found_band = bands
            if ratio == 1.0:
                multiple_matches.append(bands)

        if len(multiple_matches) > 1 and not song_name:
            print("There was multiple results with same name:", band_name)

        if song_name:
            found_band = find_band_with_song(multiple_matches, song_name)

        band.genres = found_band["genres"]
        band.name = found_band["name"]
        band.id = found_band["id"]

    else:
        print("could not find:" + name_of_band)

    if find_top_5_songs:
        find_top_5(band)

    return band


def create_playlist(playlist_name, song_list):
    new_list = []
    for song in song_list:
        new_list.append(song.id)
    song_list_split = [new_list[i:i + 100] for i in range(0, len(new_list), 100)]
    print(song_list)
    user_id = spotify.me()['id']
    playlist = spotify.user_playlist_create(user_id, playlist_name)
    for chunk in song_list_split:
        spotify.playlist_add_items(playlist["id"], chunk)


def return_list_of_artists_from_playlist(playlistID):
    playlist = spotify.playlist(playlistID)
    list: list[Artist] = []

    for line in playlist["tracks"]["items"]:
        for artist in line["track"]["artists"]:
            artist_id = artist["id"]
            artist_name = artist["name"]
            found = False
            for i in range(0, len(list)):
                if artist_id == list[i].id:
                    found = True
                    break
            if not found:
                list.append(Artist(id=artist_id, name=artist_name))
    return list


def get_song_list_from_artist_list(artists, number_of_songs):
    song_list = []
    for artist in artists:
        list_of_songs = find_top_song(artist.id, number_of_songs)
        for i in list_of_songs:
            song_list.append(i)
    return song_list


def find_top_song(artist_id, number_of_songs):
    uri = 'spotify:artist:' + artist_id
    list = []
    results = spotify.artist_top_tracks(uri)
    for track in results['tracks'][:number_of_songs]:
        song = Song()
        song.id = track["id"]
        song.name = track["name"]
        list.append(song)
    return list
