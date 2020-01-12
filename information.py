import urllib.request
from bs4 import BeautifulSoup
import sys
import math
import json
from datetime import datetime

n = int(input())

link_lr2mypage = "http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=mypage&playerid=" + str(n)
stairway_mypage = "https://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page=" + str(n)
tag_html = urllib.request.urlopen(link_lr2mypage).read().decode('shift_JIS', 'ignore')
tag_soup = BeautifulSoup(tag_html, "html.parser")
song_table=str(tag_soup.findAll("table")[0]).split("\n")
player_name = song_table[1].split('>')[4].split('<')[0]
dani_sp = song_table[3].split('>')[4].split('<')[0].split('/')[0]

html_stairway = urllib.request.urlopen(stairway_mypage).read().decode('shift_JIS', 'ignore')
soup_stairway = BeautifulSoup(html_stairway, "html.parser")
stairway_table = str(soup_stairway.findAll("table")[1]).split("\n")
clear_table = stairway_table[5].split('>')[2:]
clear_number = []

for i in range(0, len(clear_table)-2, 2):
    clear_number.append(clear_table[i].split('<')[0])


score_table= stairway_table[-5].split('>')[2:]
score_number = []

for i in range(0, len(score_table)-2, 2):
    score_number.append(score_table[i].split('<')[0])
print(score_number)
