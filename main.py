from datetime import time
from time import sleep
import numpy as np
import pandas as pd
import requests
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

url = "https://api-basketball.p.rapidapi.com/games"

headers = {
    'x-rapidapi-key': "REDACTED",
    'x-rapidapi-host': "api-basketball.p.rapidapi.com"
    }
parameters = []
parameters.append({'season':'2015-2016', 'league':'12'})
parameters.append({'season':'2016-2017', 'league':'12'})
test = {'season':'2015-2016', 'league':'12'}
dflist = []

for i in range(len(parameters)):

    response = requests.get(url, headers=headers, params=parameters[i])
    data = response.json()
    datas = json.dumps(data, indent=4)
    print(i)
    # print(len(datas))
    gameinfo = []
    def cleandata():
        for i in range(len(data['response'])):
            # Not interested in games that go into overtime
            if data['response'][i]['scores']['home']['over_time'] is None:
                # Sets 1 if hometeam wins, 0 if home team loses
                ht = data['response'][i]['scores']['home']['total']
                at = data['response'][i]['scores']['away']['total']
                winlose = ht > at

                cell = {
                    'q1h': data['response'][i]['scores']['home']['quarter_1'],
                    'q2h': data['response'][i]['scores']['home']['quarter_2'],
                    'q3h': data['response'][i]['scores']['home']['quarter_3'],
                    'q4h': data['response'][i]['scores']['home']['quarter_4'],
                    'q1a': data['response'][i]['scores']['away']['quarter_1'],
                    'q2a': data['response'][i]['scores']['away']['quarter_2'],
                    'q3a': data['response'][i]['scores']['away']['quarter_3'],
                    'q4a': data['response'][i]['scores']['away']['quarter_4'],
                    'toth':data['response'][i]['scores']['home']['total'],
                    'tota': data['response'][i]['scores']['away']['total'],
                    'winlose': winlose
                }
                gameinfo.append(cell)
        return gameinfo


    d = cleandata()


    df = pd.DataFrame(d)

    # print(df)
    # print('--------------------------------------')
    df['Tot_3qs_h']= df.iloc[:, 0:2].sum(axis=1)
    df['Tot_3qs_a']= df.iloc[:, 4:6].sum(axis=1)
    df['Tot_3qs_ha']= df['Tot_3qs_h'] + df['Tot_3qs_a']
    df['Tot_4q_ha']= df.iloc[:, 3] + df.iloc[:, 7]
    # Input: Total points in Q3 for home and away
    df['Inputs']= df['Tot_3qs_ha']
    # Output: Total points in Q4 for home and away
    df['Outputs']= df['Tot_4q_ha']
    # print(df)
    # print('--------------------------------------')
    # print('--------------------------------------')
    # print('--------------------------------------')
    dflist.append(df)

master = pd.concat([dflist[0],dflist[1]])

print(dflist)
print(master)
print(master['Tot_3qs_ha'])
print(master['Tot_4q_ha'].max())
print(master['Tot_3qs_ha'].max())
threeQarray_train = dflist[0]['Tot_3qs_ha'].to_numpy()
fourQarray_train = dflist[0]['Tot_4q_ha'].to_numpy()
threeQarray_test = dflist[1]['Tot_3qs_ha'].to_numpy()
fourQarray_test = dflist[1]['Tot_4q_ha'].to_numpy()
