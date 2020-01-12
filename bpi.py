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
    print(s)
    if(s < 0):
        return max(-pow(-s, 1/k), -15)
    else:
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

for i in range(1, 1036):
    song_id = i
    au = song_table[14 * i + 4].split('>')[2].split('<')[0] #タイトル
    try:
        my_score = int(song_table[14 * i + 7].split('>')[1].strip('</td')) #スコア
    except ValueError:
        my_score = 0
    try:
        rank = int(song_table[14 * i + 6].split('>')[1].strip('</td')) 
    except ValueError:
        rank = songs_data[str(i)]['players']
    try:
        rate = float(song_table[14 * i + 8].split('>')[1].strip('</td')) 
    except ValueError:
        rate = 0
    try:
        bp = int(song_table[14 * i + 10].split('>')[1].strip('</td'))
    except ValueError:
        bp = songs_data[str(i)]['max_score'] // 2
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
               'p':songs_data[str(i)]['p'],
               'player':songs_data[str(i)]['players']
               }
    try:
        bpi = round(max(BPI_calc(data[i]['my_score'], data[i]['average'], data[i]['zenichi'], data[i]['max_score'], data[i]['p']),-15), 2)
        BPI_list.append(bpi)
    except ValueError:
        break

sorted_BPI = sorted(BPI_list, reverse=True)
sougou = sougou_BPI(BPI_list)
print(sorted_BPI[:10])
print(sougou)


html_string = '''
<!DOCTYPE html>
    <head>
        <meta charset="UTF-8">
        <title>発狂BMS score sheet</title>
		</script>
    </head>
    <body>
        <p>This is your score.</p>
        <div id="users">
			<form action="" caption="search songs">
				<input type="text" class="search">
			</form>
            <table id="myTable" class="tablesorter">
                <thead>
                    <tr>
                        <th class="sort" data-sort="Ex">Ex</th>
                        <th class="sort" data-sort="title">title</th>
                        <th class="sort" data-sort="rank" >rank</th>
                        <th class="sort" data-sort="score">score</th>
                        <th class="sort" data-sort="BPI">BPI</th>
                        <th class="sort" data-sort="minBP">minBP</th>
                        <th class="sort" data-sort="rate">rate</th>      
                    </tr>
                </thead>
                <tbody class="list">
'''

for i in range(1, 1036):
    row = '\t\t\t\t\t<tr>\n'
    row += '\t\t\t\t\t\t<td class="Ex">' + str(data[i]['grade']) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="title">' + str(data[i]['title']) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="rank">' + str(data[i]['rank']) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="score">' + str(data[i]['my_score']) + '/' + str(data[i]['max_score']) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="BPI">' + str(BPI_list[i-1]) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="minBP">' + str(data[i]['miss_count']) + '</td>\n'
    row += '\t\t\t\t\t\t<td class="rate">' + str(data[i]['rate']) + '</td>\n'
    row += '\t\t\t\t\t</tr>\n'
    html_string += row

html_string+= '''
                </tbody>
            </table>
            <div class="pager">
                <ul class="pagination"></ul>
            </div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/list.js/1.5.0/list.min.js"></script>
        <script>
            var options = {
                valueNames:['Ex', 'title', 'rank', 'score', 'BPI', 'minBP', 'rate' ],
                page: 25,
                pagination:{
                    paginationClass:'pagination',
                    innerWindow:2,
                    outerWindow:1,
                }
            };
            var userList = new List('users', options);

            userList.on('sortStart', function(a){
                console.log(a.i);
                a.i=1;
            });
            userList.sort('title', {order : 'asc'});
        </script>

        <style>
        .sort.desc:after{
            content:'▼';
        }
        .sort.asc:after{
            content:"▲";
        }
        </style>

        <style>
            /* style for pager and pagination from http://wwx.jp/css-pagination*/
            .pager {
                overflow: hidden;
            }

            .pager ul {
                list-style: none;
                position: relative;
                left: 50%;
                float: left;
            }

            .pager ul li {
                margin: 0 1px;
                position: relative;
                left: -50%;
                float: left;
            }

            .pager ul li span,
            .pager ul li a {
                display: block;
                font-size: 16px;
                padding: 0.6em 1em;
                border-radius: 3px;
            }

            .pager ul li a {
                background: #EEE;
                color: #000;
                text-decoration: none;
            }

            .pager ul li a:hover {
                background: #333;
                color: #FFF;
            }

            /* added by myself */
            .pager ul li.active{
                font-weight: bold;
            }

            table{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            }

            table th,table td{
            padding: 10px 0;
            text-align: center;
            }

            table tr:nth-child(odd){
            background-color: #eee
            }
        </style>
    </body>
</html>
'''

with open(str(n) + '.html', 'w') as f:
    f.write(html_string)


