import urllib.request
from bs4 import BeautifulSoup
import codecs
import sys
import math
 
def cp65001(name):
    if name.lower() == 'cp65001':
        return codecs.lookup('utf-8')
codecs.register(cp65001)
 
def PGF(x,m):
    try:
        return 1+(x-0.5)/(1-x)
    except:
        return m
def BPI_calc(s,k,z,m):
    S=PGF (s/m,m)
    K=PGF (k/m,m)
    Z=PGF (z/m,m)
    S_dash=S/K
    Z_dash=Z/K
    if(s>=k):
        return 100*(pow(math.log(S_dash),1.5))/(pow(math.log(Z_dash),1.5))
    else:
        return -100*(pow(-math.log(S_dash),1.5))/(pow(math.log(Z_dash),1.5))
 
player_name=input()
path_w = player_name+'.csv'
 
s = 'New file'
 
tag_URL=""
tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"
tag_URL2 = "search.cgi?mode=search&sort=bmsid_desc&keyword="
tag_URL3 = "&exec=%8C%9F%8D%F5&type=tag"
IR_URL=""
with open(path_w, mode='w') as f:
    f.write("難易度,"+"曲名,"+"理論値,"+"全国TOP,"+player_name+"さんのスコア,"+"全国平均,"+"BPI\n")
    for i in range(0,13):#TAG:sl0~sl12
        sl="sl"+str(i)
        print ("\n"+sl+"\n")
        tag_URL=tag_URL1+tag_URL2+sl+tag_URL3
        tag_html = urllib.request.urlopen(tag_URL).read().decode('shift_JIS', 'ignore')
        tag_soup = BeautifulSoup(tag_html, "html.parser")
        href = [a.get("href") for a in tag_soup.find_all("a")]
        song_table=str(tag_soup.findAll("table")[0]).split("\n")
        song_list=[]
        HMax_list=[]
        Max_list=[]
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
         
        for IR_URL in href:#jump urlpage
            if('ranking&bmsid=' in IR_URL):
                #print IR_URL
                IR_URLs=IR_URL.split("&")
                j="1"
                now_song=song_list[count]
                 
                print  (now_song)
                Rank=1
                average_score=0
                player_score=0
                flag=True
                while True:#page1~n
                    IR_URL=tag_URL1+IR_URLs[0]+"&page="+j+"&"+IR_URLs[1]
                    #print (IR_URL)
                    IR_html=urllib.request.urlopen(IR_URL).read().decode('shift_JIS', 'ignore')
                    IR_soup = BeautifulSoup(IR_html, "html.parser")
                    try:
                        IR_list=str(IR_soup.findAll("table")[3]).split("\n")
                    except:
                        break
                     
                     
                    # print str(IR_soup.findAll("table")[3]).split("\n")
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
                                HMax_list.append(int(IR_data[5].split("/")[0]))#送信するなり
                                Max_list.append(int(IR_data[6].split("/")[1])*2)#書き込むなり
                                 
                            if(IR_data[1]==player_name):
                                player_score_list.append(int(IR_data[5].split("/")[0]))
                                flag=False
                            Rank+=1
                            average_score+=int(IR_data[5].split("/")[0])
                    j=str(int(j)+1)
 
                if(flag):
                    player_score_list.append(0)
                average_score=average_score/Rank
                average_score_list.append(average_score)#平均スコア
                 
                print ("理論値:"+str(Max_list[count]))
                print ("全1   :"+str(HMax_list[count]))
                print ("スコア:"+str(player_score_list[count])) 
                print ("平均  :"+str(round(average_score_list[count],2)))
                BPI="不明"
                if(player_score_list[count]!=0):
                    BPI=round(BPI_calc(player_score_list[count],average_score_list[count],HMax_list[count],Max_list[count]),2)
                player_BPI_list.append(BPI)
                f.write(sl+","+now_song+","+str(Max_list[count])+","+str(HMax_list[count])+","+str(player_score_list[count])+","+str(round(average_score_list[count],2))+","+str(BPI)+"\n")
                print("BPI:"+str(BPI))
                Rank_list.append(Rank)#プレイ人数
                count+=1