import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import sys
import math
import urllib.request

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


n = int(input())

url_stairway = "http://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page="

with open("songs.json", "r") as f:
    song = json.load(f)
url = url_stairway + str(n)
tag_html = urllib.request.urlopen(url).read().decode('shift_JIS', 'ignore')
tag_soup = BeautifulSoup(tag_html, "html.parser")
href = [a.get("href") for a in tag_soup.find_all("a")]
song_table=str(tag_soup.findAll("table")[5]).split("\n")

my_data = {}

for i in range(1035):
    song_id = i + 1
    au = song_table[14 * i + 18].split('>')[2].split('<')[0] #タイトル
    my_score = int(song_table[14 * i + 21].split('>')[1].strip('</td')) #スコア
    rank = int(song_table[14 * i + 20].split('>')[1].strip('</td')) 
    rate = float(song_table[14 * i + 22].split('>')[1].strip('</td')) 
    bp = int(song_table[14 * i + 24].split('>')[1].strip('</td'))
    my_data[song_id] = {"title":au, "score":my_score, "rank":rank, "score_rate":rate, "miss_count":bp}


'''
print(song_table[18])#タイトル
print(song_table[20])#順位
print(song_table[21])#EXスコア
print(song_table[22])#レート
print(song_table[24])#BP
print("--------------")
print(song_table[32])
print(song_table[34])
print(song_table[35])
print(song_table[36])
print(song_table[38])
print("-------------")
'''