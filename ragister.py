import urllib.request
from bs4 import BeautifulSoup
import sys
import math
import json
from datetime import datetime

now1 = datetime.now()

 
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

songs = {}
BPI_per = [0.0003791, 0.0008341, 0.0018335, 0.00403067, 0.00886266, 0.01948992, 0.04286059, 0.09425297, 0.2072687]
 
tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"
with open("songs.json", 'w') as f:
    for i in range(1,26):#TAG:★1~26
        sl="★"+str(i)
        print ("\n"+sl+"\n")
        tag_URL="http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=search&type=insane&exlevel=" + str(i) + "&7keys=1"
        tag_html = urllib.request.urlopen(tag_URL).read().decode('shift_JIS', 'ignore')
        tag_soup = BeautifulSoup(tag_html, "html.parser")
        href = [a.get("href") for a in tag_soup.find_all("a")]
        song_table=str(tag_soup.findAll("table")[0]).split("\n")
        song_list=[]#song_title
        HMax_list=[]#?
        Max_list=[]#?
        average_score_list=[]
        Rank_list=[]
        player_score_list=[]
        player_BPI_list=[]
        for song in song_table:#song_name_get
            if('<td width="20%"><a href="search.cgi?mode=ranking' in song):
                song=song[16:]
                song=song.split(">")[1][:-3]
                song_list.append(song)
        
        count=0
        for IR_URL in href:#曲の数だけ
            if('ranking&bmsid=' in IR_URL):#SP★1~???, DP★1~???のリンクを省く
                #print IR_URL
                IR_URLs=IR_URL.split("&")
                j=1
                now_song=song_list[count]
                print(now_song)
                Rank=1
                average_score=0
                player_score=0
                players_count = 0
                flag_bug = False
                BPI_rank = []
                BPI_score = []
                flag=True
                while True:#page1~n
                    IR_URL=tag_URL1+IR_URLs[0]+"&page="+str(j)+"&"+IR_URLs[1]
                    IR_html=urllib.request.urlopen(IR_URL).read().decode('shift_JIS', 'ignore')
                    IR_soup = BeautifulSoup(IR_html, "html.parser")
                    try:
                        IR_list=str(IR_soup.findAll("table")[3]).split("\n")
                    except:
                        break
                    if(players_count == 0):
                        IR_number=str(IR_soup.findAll("table")[1]).split("\n")
                        player = IR_number[3].strip('</td>').split('<td>')
                        player = int(player[1].strip('</td>'))
                        players_count += 1
                        for bpn in BPI_per:
                            rank_append = math.ceil(bpn * player)
                            if(rank_append == 1 or (rank_append in BPI_rank)):
                                rank_append += 1
                            BPI_rank.append(math.ceil(bpn * player))
                        print(BPI_rank)
                    for IR_player in IR_list:#table cleaning
                        if('<tr><td align="center" rowspan="2">' in IR_player):
                            IR_data=IR_player.split("<td>")
                            IR_data[0]=IR_data[0][35:]
                            IR_data[1]=IR_data[1][:-4]
                            for k in range(len(IR_data)):#IR_data get 
                                IR_data[k]=IR_data[k][:-5]
                                index=IR_data[k].find('>')
                                IR_data[k]=IR_data[k][index+1:]
                                #print (IR_data[k])
                            if(Rank==1):
                                zenichi = int(IR_data[5].split("/")[0])
                            if(Rank==2):
                                max_score = int(IR_data[6].split("/")[1])*2
                                Max_list.append(max_score)#書き込むなり
                                if(zenichi > max_score):
                                    zenichi = int(IR_data[5].split("/")[0])
                                HMax_list.append(zenichi)
                            if(Rank in BPI_rank):
                                sc = int(IR_data[5].split("/")[0])
                                BPI_score.append(sc)
                            Rank+=1
                            average_score+=int(IR_data[5].split("/")[0])
                    j += 1
                average_score=average_score/Rank
                average_score_list.append(average_score)#平均スコア
                print("プレイ人数:" + str(player)) 
                print ("理論値:"+str(Max_list[count]))
                print ("全1   :"+str(HMax_list[count]))
                print ("平均  :"+str(round(average_score_list[count],2)))
                print(BPI_score) #理論BPI値
                BPI_otehon = [90, 80, 70, 60, 50, 40, 30, 20, 10]
                great_p = 1.8
                min_bunsan = 1e9
                for i in range(1, 1001):
                    BPI_zissai = []
                    i /= 100
                    for bs in BPI_score:
                        if(bs <= max_score):
                            BPI_zissai.append(BPI_calc(bs,average_score,zenichi,max_score,i))
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
                    BPI_kekka.append(BPI_calc(bs,average_score,zenichi,max_score,great_p))
                print(BPI_kekka)
                songs[now_song] = {"grade":sl.strip("★") , "max_score":max_score, "zenichi":zenichi, "average":average_score, "p":great_p, "players":player}
                count+=1
    json.dump(songs, f, ensure_ascii=False, indent=4)

now2 = datetime.now()
total_time = now2 - now1
print("実行時間:" + str(total_time))