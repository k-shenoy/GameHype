import numpy as np
import pandas as pd
import requests
import json



myfile= open('gamedates.csv')
data=myfile.read().split("\n")
myfile.close

list1 = []

for date in data:

    url= 'https://api.sportsdata.io/v3/nba/scores/json/TeamGameStatsByDate/'+date+'?key=bdee52c0360f470dabff60659690c9e3'
    #print(url)
    r = requests.get(url).json()
##    print("===========")
##    print(r)
##    print("=========")
    #print(r)
    #dicts = [json.loads(d) for d in r]
    for dicts in r:
        if (type(dicts))== dict:
        #print(dicts)
            dict1={}
                #gamedict.add(dicts, "Day", "AwayTeam")
            dict1={"Day": (dicts['Day']), \
              "Team":(dicts["Team"]), \
              "TeamID":(dicts['TeamID']), \
              "Assists":(dicts["Assists"]), \
              "BlockedShots":(dicts["BlockedShots"]), \
              "DefensiveRebounds":(dicts['DefensiveRebounds']), \
              "DoubleDoubles":(dicts["DoubleDoubles"]), \
              "EffectiveFieldGoalsPercentage":(dicts["EffectiveFieldGoalsPercentage"]), \
              "FieldGoalsAttempted":(dicts["FieldGoalsAttempted"]), \
              "FieldGoalsPercentage":(dicts["FieldGoalsPercentage"]), \
              "FreeThrowsPercentage":(dicts["FreeThrowsPercentage"]), \
              "OffensiveRebounds":(dicts["OffensiveRebounds"]), \
              "PersonalFouls":(dicts["PersonalFouls"]), \
              "PlusMinus":(dicts["PlusMinus"]), \
              "Points":(dicts["Points"]), \
              "Possessions":(dicts["Possessions"]), \
              "Rebounds":(dicts["Rebounds"]), \
              "Steals":(dicts["Steals"]), \
              "ThreePointersPercentage":(dicts["ThreePointersPercentage"]), \
              "TripleDoubles":(dicts["TripleDoubles"]), \
              "TrueShootingPercentage":(dicts["TrueShootingPercentage"]), \
              "Turnovers":(dicts["Turnovers"]), \
              "TwoPointersPerctenage":(dicts["TwoPointersPercentage"])}
            #print("yes")
            list1.append(dict1)
        #print(dicts["day"])
        #print(list1)

stats= pd.DataFrame(list1)
stats.to_csv('stats20.csv', index=False) 
    

