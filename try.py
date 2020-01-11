import urllib.request
from bs4 import BeautifulSoup
import sys
import math
import json
from datetime import datetime

black_list = [114328, 108312, 141249, 114453, 111571, 113171, 113693]
BPI_per = [0.0003791, 0.0008341, 0.0018335, 0.00403067, 0.00886266, 0.01948992, 0.04286059, 0.09425297, 0.2072687]
song_id = [1029, 1030]

songs = {}
def PGF(x,m):
    try:
        return 1+(x-0.5)/(1-x)
    except:
        return m

def BPI_calc(s,k,z,m,p):
    S=PGF(s/m,m)
    K=PGF(k/m,m)
    Z=PGF(z/m,m)
    S_dash=S/K
    Z_dash=Z/K
    if(s>=k):
        return 100*(pow(math.log(S_dash),p))/(pow(math.log(Z_dash),p))
    else:
        return -100*(pow(-math.log(S_dash),p))/(pow(math.log(Z_dash),p))

song_list = []
tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"
link = "http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=search&type=insane&exlevel=7&7keys=1"
tag_html = urllib.request.urlopen(link).read().decode('shift_JIS', 'ignore')
tag_soup = BeautifulSoup(tag_html, "html.parser")
song_table=str(tag_soup.findAll("table")[0]).split("\n")
n = len(song_table) // 10
for i in range(n):#song_name_get
    song_list.append(song_table[10 * i + 5].split('>')[2].split('<')[0])
href = [a.get("href") for a in tag_soup.find_all("a")][50:-1]
so = 0
IR_URL = href[16]
print(IR_URL)
page = 1
BPI_rank = []#理想BPIを格納
ranking_data = [] #スコア
IR_URLs=IR_URL.split("&")
Rank=1
max_record = 2
while True:#page1~n
    IR_URL=tag_URL1+IR_URLs[0]+"&page="+str(page)+"&"+IR_URLs[1]
    IR_html=urllib.request.urlopen(IR_URL).read().decode('shift_JIS', 'ignore')
    IR_soup = BeautifulSoup(IR_html, "html.parser")
    try:
        IR_list=str(IR_soup.findAll("table")[3]).split("\n")[2:-1][0::2]
        if(max_record):
            max_score = int(IR_list[0].split('>')[14].split('/')[1].split('(')[0])
            max_record -= 1
    except:
        break
    for IR_player in IR_list:
        IR = IR_player.split('>')
        player_ID = int(IR[4].split("=")[3].strip('"'))
        if(player_ID in black_list):
            continue
        else:
            player_score = int(IR[14].split('/')[0])
            score_rate = float(IR[14].split('/')[1].split('(')[1].split('%')[0])
            if(score_rate >= 62):
                ranking_data.append(player_score)
            elif(len(ranking_data) == 0):
                continue
            else:
                break
    page += 1
while ranking_data[0] > max_score:
    ranking_data.pop(0)
zenichi = ranking_data[0]
average = sum(ranking_data) / len(ranking_data)
players = len(ranking_data)
print("理論値:" + str(max_score))
print("全1:" + str(zenichi))
print("平均:" + str(average))
print("プレイ人数:" + str(len(ranking_data)))
for bpn in BPI_per:
    rank_append = math.ceil(bpn * players)
    if(rank_append == 1):
        rank_append += 1
    if(rank_append in BPI_rank):
        rank_append = max(BPI_rank) + 1
    BPI_rank.append(rank_append)
BPI_score = []
for bp in BPI_rank:
    BPI_score.append(ranking_data[bp + 1])
print(BPI_score)
BPI_otehon = [90, 80, 70, 60, 50, 40, 30, 20, 10]
great_p = 1.8
min_bunsan = 1e9
for i in range(1, 3001):
    BPI_zissai = []
    i /= 1000
    for bs in BPI_score:
        if(bs <= max_score):
            BPI_zissai.append(BPI_calc(bs,average,zenichi,max_score,i))
        else:
            BPI_zissai.append(90)
    bunsan = 0
    for j in range(len(BPI_score)):
        bunsan += (BPI_otehon[j] - BPI_zissai[j])**2
    if(min_bunsan > bunsan):
        great_p = i
        min_bunsan = bunsan
print("理想のp値:" + str(great_p))
BPI_kekka = []
for bs in BPI_score:
    BPI_kekka.append(BPI_calc(bs,average,zenichi,max_score,great_p))
songs[song_id[so]] = {"grade":3, "max_score":max_score, "zenichi":zenichi, "average":average, "p":max(0.8, great_p), "players":len(ranking_data)}
so += 1