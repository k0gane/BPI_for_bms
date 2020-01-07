import urllib.request
from bs4 import BeautifulSoup
import sys
import math
import json
tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"

songs = {}
BPI_per = [0.0003791, 0.0008341, 0.0018335, 0.00403067, 0.00886266, 0.01948992, 0.04286059, 0.09425297, 0.2072687]

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

IR_URL="http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&page=1&bmsid=229189"
IR_html=urllib.request.urlopen(IR_URL).read().decode('shift_JIS', 'ignore')
IR_soup = BeautifulSoup(IR_html, "html.parser")
IR_table = IR_soup.findAll("table")
IR_list=str(IR_soup.findAll("table")[1]).split("\n")
player = IR_list[3].strip('</td>').split('<td>')
player = player[1].strip('</td>')
print(player)
