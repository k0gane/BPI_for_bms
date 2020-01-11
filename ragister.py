import urllib.request
from bs4 import BeautifulSoup
import sys
import math
import json
from datetime import datetime

now1 = datetime.now()
black_list = [114328, 108312, 141249, 114453, 111571, 113171, 113693]
song_id =  [49,3,19,52,1,31,37,48,21,6,8,5,39,46,45,53,4,40,47,26,42,23,32,38,44,29,35,43,25,17,15,2,22,41,10,16,50,51,7,11,27,24,34,33,14,30,9,36,20,12,18,28,13,
            56,78,85,79,104,107,67,54,71,100,59,91,83,58,72,62,92,105,55,76,70,68,93,69,87,95,80,82,73,108,98,74,81,103,97,64,66,75,65,94,88,102,99,63,86,61,109,60,106,96,84,89,101,90,57,77,
            125,116,159,113,122,157,161,136,139,162,153,149,154,115,112,160,127,118,150,158,124,131,114,135,126,133,146,132,147,134,140,117,119,148,143,144,152,129,130,123,155,120,111,137,141,145,138,121,156,110,128,142,151,
            208,168,196,197,177,183,166,182,179,192,193,202,195,200,210,165,189,187,167,163,207,171,209,164,180,184,190,204,185,201,174,198,205,212,172,213,206,188,173,211,169,199,170,214,178,186,176,203,191,194,175,181,
            262,240,257,219,233,273,215,268,235,255,220,222,269,246,252,266,227,244,245,236,232,248,221,256,267,265,247,238,241,270,223,217,226,261,228,239,259,249,230,264,263,216,272,260,254,242,253,271,224,231,243,258,225,229,237,251,218,234,250,
            282,275,278,314,319,318,289,287,302,316,281,274,280,304,293,305,277,313,311,297,298,294,306,303,295,300,312,286,296,310,299,279,283,301,290,288,285,315,291,276,317,292,308,284,307,309,
            333,357,364,365,345,353,340,377,334,343,375,378,323,335,342,371,363,370,327,326,366,320,367,362,355,359,354,369,330,339,324,356,328,344,329,321,338,351,379,336,360,350,341,332,347,372,352,346,358,373,361,349,374,368,337,331,376,325,348,322,
            424,381,391,407,384,425,415,410,426,409,417,422,423,382,401,387,392,398,411,397,400,416,380,414,385,389,420,405,396,402,406,403,393,394,388,399,390,383,395,421,419,418,404,412,386,408,413,
            429,463,468,432,450,444,441,472,464,457,428,435,431,454,469,440,471,446,448,462,452,443,427,461,433,453,455,465,470,434,467,447,460,445,456,458,438,449,430,466,442,459,437,451,436,439,
            475,503,499,477,474,485,480,531,492,487,505,525,530,491,473,528,488,512,489,529,501,482,533,536,516,494,486,506,502,481,484,504,483,517,518,500,524,498,497,510,495,496,532,507,521,523,526,535,479,509,519,508,493,527,522,514,515,490,520,534,476,478,513,511,
            581,576,570,540,577,558,538,567,572,547,539,543,573,552,561,545,537,554,542,541,565,578,562,580,556,548,557,563,555,571,574,549,579,564,544,569,560,575,559,566,553,550,551,568,546,
            583,639,615,613,624,588,605,621,623,594,626,593,601,582,600,637,602,587,625,606,636,631,608,635,629,627,630,638,586,596,614,599,610,595,628,611,607,618,603,633,620,632,634,604,597,591,584,622,609,617,616,592,598,619,585,590,612,589,
            655,642,660,665,644,653,681,668,656,670,684,673,680,664,650,676,662,663,685,659,654,645,640,683,675,647,667,658,679,682,672,657,646,648,661,643,649,677,651,641,669,652,674,666,671,678,
            686,692,715,725,717,707,699,689,719,698,710,691,705,720,702,697,695,693,722,714,716,724,708,721,690,728,704,687,709,718,688,694,696,712,703,701,700,726,711,706,723,713,727,
            758,762,747,743,746,744,741,763,729,742,732,755,759,754,751,739,761,750,745,731,737,753,748,738,757,756,730,752,733,735,734,736,749,760,740,
            783,765,771,770,790,793,776,794,784,772,775,789,764,768,774,785,781,787,778,766,777,788,792,791,779,767,786,773,769,780,782,
            802,799,810,816,823,818,817,800,797,795,804,796,812,805,806,814,824,801,819,798,815,821,813,822,808,811,803,820,807,809,
            827,849,843,853,852,830,851,833,838,839,850,848,840,828,841,846,836,825,834,845,832,837,835,831,847,826,844,829,842,
            858,873,855,870,876,857,854,872,860,888,861,881,889,879,885,859,878,864,862,886,880,874,877,882,875,863,884,865,887,856,866,868,871,867,883,869,
            891,912,923,915,892,909,902,905,895,903,910,897,907,916,908,926,919,900,913,911,901,917,924,893,898,914,921,904,920,918,890,899,925,906,922,894,896,
            943,949,933,938,929,952,954,951,955,946,940,956,927,941,945,959,931,939,928,936,944,961,962,950,932,947,934,958,930,948,935,942,957,937,953,963,960,
            978,976,970,981,977,987,975,989,964,984,982,985,971,966,988,967,986,980,965,973,979,969,974,972,968,983,
            1010,1000,1017,999,998,1011,1013,1015,1004,990,993,1003,1014,991,995,1001,994,1016,997,1002,1009,1006,992,1008,1012,996,1007,1005,
            1024,1018,1023,1022,1021,1020,1025,1019,1027,1028,1026,
            1029,1030,
            1033,1035,1034,1032,1031]
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
diff = [i for i in range(1, 26)]
border = [71 - (i*1.5) for i in range(25)]
border.append(40)
diff.append(99)
songs = {}
un = 0
BPI_per = [0.0003791, 0.0008341, 0.0018335, 0.00403067, 0.00886266, 0.01948992, 0.04286059, 0.09425297, 0.2072687]
tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"
so = 0
with open("songs.json", 'w') as f:
    for dif in diff:#TAG:★1~25, 99
        song_list = []
        print ("\n LEVEL "+str(dif)+"\n")
        tag_URL="http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=search&type=insane&exlevel=" + str(dif) + "&7keys=1"
        tag_html = urllib.request.urlopen(tag_URL).read().decode('shift_JIS', 'ignore')
        tag_soup = BeautifulSoup(tag_html, "html.parser")
        href = href = [a.get("href") for a in tag_soup.find_all("a")][50:-1]
        song_table=str(tag_soup.findAll("table")[0]).split("\n")
        n = len(song_table) // 10
        for s in range(n):#song_name_get
            song_list.append(song_table[10 * s + 5].split('>')[2].split('<')[0])
        for w in range(len(href)):#曲の数だけ
            max_record = 2
            page = 1
            BPI_rank = []#理想BPIを格納
            ranking_data = [] #スコア
            IR_URLs=href[w].split("&")
            Rank=1
            print(song_list[w])
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
                        if(score_rate >= border[un]):
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
            BPI_otehon = [90, 80, 70, 60, 50, 40, 30, 20, 10]
            great_p = 1.8
            min_bunsan = 1e9
            for kouho_p in range(1, 2501):
                BPI_zissai = []
                kouho_p /= 1000
                for bs in BPI_score:
                    if(bs <= max_score):
                        BPI_zissai.append(BPI_calc(bs,average,zenichi,max_score,kouho_p))
                    else:
                        BPI_zissai.append(90)
                bunsan = 0
                for j in range(len(BPI_score)):
                    bunsan += (BPI_otehon[j] - BPI_zissai[j])**2
                if(min_bunsan > bunsan):
                    great_p = kouho_p
                    min_bunsan = bunsan
            print("理想のp値:" + str(great_p))
            BPI_kekka = []
            for bs in BPI_score:
                BPI_kekka.append(BPI_calc(bs,average,zenichi,max_score,great_p))
            songs[song_id[so]] = {"grade":dif, "max_score":max_score, "zenichi":zenichi, "average":average, "p":great_p, "players":len(ranking_data)}
            print(song_id[so])
            print(songs[song_id[so]])
            so += 1
        un += 1
        print(len(songs))
    print(len(songs))
    json.dump(songs, f, ensure_ascii=False, indent=4)

now2 = datetime.now()
total_time = now2 - now1
print("実行時間:" + str(total_time))