import urllib.request
from bs4 import BeautifulSoup
import sys

tag_URL1 = "http://www.dream-pro.info/~lavalse/LR2IR/"

IR_URL="http://www.dream-pro.info/~lavalse/LR2IR/search.cgi?mode=ranking&page=1&bmsid=66"
IR_html=urllib.request.urlopen(IR_URL).read().decode('shift_JIS', 'ignore')
IR_soup = BeautifulSoup(IR_html, "html.parser")
IR_table = IR_soup.findAll("table")
IR_list=str(IR_soup.findAll("table")[1]).split("\n")
player = IR_list[3].strip('</td>').split('<td>')
player = player[1].strip('</td>')
print(player)
