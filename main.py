import spotify

with open("bands.txt") as file:
    lines = [line.rstrip() for line in file]

song_list = []

for line in lines:
    result = spotify.find_band(line, True)
    print(result.name, " ", result.genres, ": ", end="")

    for songs in result.top_5_songs:
        print(songs.name, ", ", end="")
        song_list.append(songs.id)
    print()

spotify.create_playlist("ArcTanGent2023", song_list)
