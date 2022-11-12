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

exit()





#['6QN0mXlZOwfQoFs5yu55Pg', '79xLxZrpdURjzJmdHKB85a', '6DUvpC2bFViefEhZ65NGgk', '5gXKwH68RrWzpf6DdPa3vM', '6fcCbjJDY2nJBXZccXGMi5',