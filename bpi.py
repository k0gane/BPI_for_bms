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
        return max(-100*(pow(-math.log(S_dash),p))/(pow(math.log(Z_dash),p)), -15)

def sougou_BPI(BPI_list):
    n = len(BPI_list)
    k = math.log2(n)
    s = 0
    for i in range(n):
        if(BPI_list[i] < 0):
            s -= pow(-BPI_list[i], k)
        else:
            s += pow(BPI_list[i], k)
    s /= n
    return pow(s, 1/k)


n = int(input())

url_stairway = "http://stairway.sakura.ne.jp/bms/LunaticRave2/?contents=player&page="

with open("songs.json", "r") as f:
    songs_data = json.load(f)

url = url_stairway + str(n)
tag_html = urllib.request.urlopen(url).read().decode('shift_JIS', 'ignore')
tag_soup = BeautifulSoup(tag_html, "html.parser")
song_table=str(tag_soup.findAll("table")[5]).split("\n")
my_data = {}

for i in range(1035):
    song_id = i + 1
    au = song_table[14 * i + 18].split('>')[2].split('<')[0] #タイトル
    my_score = int(song_table[14 * i + 21].split('>')[1].strip('</td')) #スコア
    rank = int(song_table[14 * i + 20].split('>')[1].strip('</td')) 
    rate = float(song_table[14 * i + 22].split('>')[1].strip('</td')) 
    bp = int(song_table[14 * i + 24].split('>')[1].strip('</td'))
    my_data[str(song_id)] = {"title":au, "score":my_score, "rank":rank, "score_rate":rate, "miss_count":bp}
BPI_list = []
data = {}
for i in range(1, 1036):
    data[i] = {'grade':songs_data[str(i)]['grade'], 
               'title':my_data[str(i)]['title'],
               'max_score':songs_data[str(i)]['max_score'],
               'zenichi':songs_data[str(i)]['zenichi'],
               'average':songs_data[str(i)]['average'],
               'my_score':my_data[str(i)]['score'],
               'rate':my_data[str(i)]['score_rate'],
               'rank':my_data[str(i)]['rank'],
               'miss_count':my_data[str(i)]['miss_count'],
               'p':songs_data[str(i)]['p']
               }
    try:
        bpi = BPI_calc(data[i]['my_score'], data[i]['average'], data[i]['zenichi'], data[i]['max_score'], data[i]['p'])
    except ValueError:
        print(data[i])
        break
    print(bpi)



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