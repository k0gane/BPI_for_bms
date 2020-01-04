import requests
from bs4 import BeautifulSoup as bp
import csv

for i in range(1, 26):
    r = requests.get("http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=search&type=insane&exlevel=" + str(i) + "&7keys=1")

    soup = bp(r.content, "html.parser")
    song_list = []
    elems = soup.select("a")
    cnt = 0
    for elem in elems:
        cnt += 1
        if(cnt >= 46):
            if(("(H)" in elem.text) or ("(A)" in elem.text) or("(黒)" in elem.text)):
                song_list.append(elem.text)
        if(elem.text == "snow storm(黒)"):
            break
    with open("song_list.txt", "w", newline="") as f:
        for song in song_list:
            f.write(str(song) + "\n")