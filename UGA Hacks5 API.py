import numpy as np
import pandas as pd
import requests
import json

url= "https://api.sportsdata.io/v3/nba/scores/json/Games/%7B2020%7D?key=5b13809bf6734452b55d4838237031cf"
r = requests.get(url).json()
##r = json.dumps(r, indent=4, sort_keys=True)
##print(r)
gamedict={}
list1 = []


for dicts in r:
    dicts1={}
    #gamedict.add(dicts, "Day", "AwayTeam")
    dicts1={"Date": (dicts["Day"]), \
                  "AwayTeam":(dicts["AwayTeam"]), \
                  "AwayTeamID":(dicts['AwayTeamID']), \
                  "AwayTeamScore":(dicts["AwayTeamScore"]), \
                  "HomeTeam":(dicts["HomeTeam"]), \
                  "HomeTeamID":(dicts['HomeTeamID']), \
                  "HomeTeamScore":(dicts["HomeTeamScore"])}
    list1.append(dicts1)

stats= pd.DataFrame(list1)

stats.to_csv('gamestats2020.csv', index=False) 
    
