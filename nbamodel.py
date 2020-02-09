import numpy as np
import pandas as pd
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
import sys

def predictScoreDiffByTeam(name1, name2):
    weights_file = 'Weights-500--11.01326.hdf5' # choose the best checkpoint
    NN_model.load_weights(weights_file) # load it
    NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
    vNum = hashc[name1]
    hNum = hashc[name2]
    row = pd.DataFrame([[winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
            ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
            ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
            attArr[vNum]/numHomeGameArr[vNum] - attArr[hNum]/numHomeGameArr[hNum]]],
            columns = ['ARD', 'APFD', 'APAD', 'AAD'])
    return predictWithData(row)

def predictAttendByTeam(name1, name2):
    weights_file2 = 'Weights-497--1940.72971.hdf5' # choose the best checkpoint
    NN_model.load_weights(weights_file2) # load it
    NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
    vNum = hashc[name1]
    hNum = hashc[name2]
    row = pd.DataFrame([[winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
            ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
            ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
            predictScoreDiffByTeam(name1, name2)]],
            columns = ['ARD', 'APFD', 'APAD', 'PTD'])
    return predictWithData(row)

def predictWithData(matchup):
    pred = NN_model.predict(matchup)
    return pred

hashc = {"AtlantaHawks":0,
"BostonCeltics":1,
"BrooklynNets":2,
"CharlotteHornets":3,
"ChicagoBulls":4,
"ClevelandCavaliers":5,
"DallasMavericks":6,
"DenverNuggets":7,
"DetroitPistons":8,
"GoldenStateWarriors":9,
"HoustonRockets":10,
"IndianaPacers":11,
"LosAngelesClippers":12,
"LosAngelesLakers":13,
"MemphisGrizzlies":14,
"MiamiHeat":15,
"MilwaukeeBucks":16,
"MinnesotaTimberwolves":17,
"NewOrleansPelicans":18,
"NewYorkKnicks":19,
"OklahomaCityThunder":20,
"OrlandoMagic":21,
"Philadelphia76ers":22,
"PhoenixSuns":23,
"PortlandTrailBlazers":24,
"SacramentoKings":25,
"SanAntonioSpurs":26,
"TorontoRaptors":27,
"UtahJazz":28,
"WashingtonWizards":29}

def start(str1,str2,type):
    df = pd.read_excel("GameData2019.xlsx")
    winArr = np.zeros(30)
    ptsForArr = np.zeros(30)
    ptsAgainstArr = np.zeros(30)
    attArr = np.zeros(30)
    numGameArr = np.zeros(30)
    numHomeGameArr = np.zeros(30)

    cumDf = pd.DataFrame([[0,0,0,0,0]],columns=['PTD', 'ARD', 'APFD', 'APAD', 'AAD'])
    for i in range(0, 1311):
      vNum = hashc[df.visit[i]]
      hNum = hashc[df.home[i]]
      if df.vpts[i] > df.hpts[i]:
        winNum = hashc[df.visit[i]]
        loseNum = hashc[df.home[i]]
      else:
        winNum = hashc[df.home[i]]
        loseNum = hashc[df.visit[i]]
      if numGameArr[loseNum]>=5 and numGameArr[winNum]>=5:
        row = pd.DataFrame([[df.vpts[i] - df.hpts[i],
              winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
              ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
              ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
              attArr[vNum]/numHomeGameArr[vNum] - attArr[hNum]/numHomeGameArr[hNum]]],
              columns = ['PTD', 'ARD', 'APFD', 'APAD', 'AAD'])
        cumDf = cumDf.append(row, ignore_index=True)

      #update winning team's wins
      winArr[winNum] = winArr[winNum] + 1

      #update visiting team other stats
      ptsForArr[vNum] = ptsForArr[vNum] + df.vpts[i]
      ptsAgainstArr[vNum] = ptsAgainstArr[vNum] + df.hpts[i]
      numGameArr[vNum] = numGameArr[vNum] + 1

      #update home team other stats
      ptsForArr[hNum] = ptsForArr[hNum] + df.hpts[i]
      ptsAgainstArr[hNum] = ptsAgainstArr[hNum] + df.vpts[i]
      attArr[hNum] = attArr[hNum] + df.att[i]
      numGameArr[hNum] = numGameArr[hNum] + 1
      numHomeGameArr[hNum] = numHomeGameArr[hNum] + 1

    cumu = cumDf
    target = cumu.PTD
    cumu.drop(['PTD'],axis = 1, inplace = True)

    NN_model = Sequential()

# The Input Layer :
#NN_model.add(Dropout(0.2, input_shape=(cumu.shape[1],)))
    NN_model.add(Dense(128, kernel_initializer='normal',input_dim = cumu.shape[1], activation='relu'))
#NN_model.add(Dense(128, kernel_initializer='normal', activation='relu'))

# The Hidden Layers :
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))

# The Output Layer :
    NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

    if (type == "score"):
        vNum = hashc[str1]
        hNum = hashc[str2]
        row = pd.DataFrame([[winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
                ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
                ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
                attArr[vNum]/numHomeGameArr[vNum] - attArr[hNum]/numHomeGameArr[hNum]]],
                columns = ['ARD', 'APFD', 'APAD', 'AAD'])
        return network(NN_model, row, "Weights-500--11.01326.hdf5")
    if (type == "attend"):
        print("hello")
        vNum = hashc[str1]
        hNum = hashc[str2]
        row2 = pd.DataFrame([[winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
                ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
                ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
                attArr[vNum]/numHomeGameArr[vNum] - attArr[hNum]/numHomeGameArr[hNum]]],
                columns = ['ARD', 'APFD', 'APAD', 'AAD'])
        psdbt = network(NN_model, row2, "Weights-500--11.01326.hdf5")
        vNum = hashc[str1]
        hNum = hashc[str2]
        row3 = pd.DataFrame([[winArr[vNum]/numGameArr[vNum] - winArr[hNum]/numGameArr[hNum],
                ptsForArr[vNum]/numGameArr[vNum] - ptsForArr[hNum]/numGameArr[hNum],
                ptsAgainstArr[vNum]/numGameArr[vNum] - ptsAgainstArr[hNum]/numGameArr[hNum],
                psdbt]],
                columns = ['ARD', 'APFD', 'APAD', 'PTD'])
        return network(NN_model, row3, "Weights-497--1940.72971.hdf5")
def network(net, row, weight):
    weights_file = weight # choose the best checkpoint
    net.load_weights(weights_file) # load it
    net.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
    return net.predict(row)[0][0]
