from difflib import SequenceMatcher
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def find_band(name_of_band, spotify_handler):
    class Band:
        name = ""
        genres = []
        id = ""
        found = False
    band = Band()

    results = spotify.search(q="artist: " + name_of_band, type="artist", limit=20)

    items = results["artists"]["items"]

    if len(items):
        found_band = None
        best_ratio = 0

        for bands in items:
            #print(bands["name"])
            ratio = similar(bands["name"].lower(), name_of_band.lower())
            # print(ratio)
            if ratio > best_ratio:
                best_ratio = ratio
                found_band = bands

        band.genres = found_band["genres"]
        band.name = found_band["name"]
        band.id = found_band["id"]
    else:
        print("could not find:" + name_of_band)
    return band


with open("bands.txt") as file:
    lines = [line.rstrip() for line in file]

load_dotenv()
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

for line in lines:
    result = find_band(line, spotify)
    print(result.name, result.genres, result.id)



