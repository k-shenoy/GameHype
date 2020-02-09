import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout
import sys

def start(str1, str2):
    df = pd.read_excel("nfldata.xlsx")
    winArr = np.zeros(32)
    ptsArr = np.zeros(32)
    ydsArr = np.zeros(32)
    toArr = np.zeros(32)

    cumDf = pd.DataFrame([[0,0,0,0,0,0]],columns=['week', 'ptDiff', 'recordDiff', 'cumPtDiffDiff', 'cumYdsDiff', 'cumToDiff'])
    for i in range(0, 266):
        winNum = hashC(df.win[i])
        loseNum = hashC(df.lose[i])
        if (df.Week[i] != 1):
            row = pd.DataFrame([[df.Week[i],
                df.PtsW[i] - df.PtsL[i],
                winArr[winNum] - winArr[loseNum],
                ptsArr[winNum] - ptsArr[loseNum],
                ydsArr[winNum] - ydsArr[loseNum],
                toArr[winNum] - toArr[loseNum]]],
                columns = ['week', 'ptDiff', 'recordDiff', 'cumPtDiffDiff', 'cumYdsDiff', 'cumToDiff'])
            cumDf = cumDf.append(row, ignore_index=True)

  #update winning team stats
    winArr[winNum] = winArr[winNum] + 1
    ptsArr[winNum] = ptsArr[winNum] + df.PtsW[i] - df.PtsL[i]
    ydsArr[winNum] = ydsArr[winNum] + df.YdsW[i] - df.YdsL[i]
    toArr[winNum] = toArr[winNum] + df.TOW[i] - df.TOL[i]

  #update losing team stats
    winArr[loseNum] = winArr[loseNum]
    ptsArr[loseNum] = ptsArr[loseNum] - df.PtsW[i] + df.PtsL[i]
    ydsArr[loseNum] = ydsArr[loseNum] - df.YdsW[i] + df.YdsL[i]
    toArr[loseNum] = toArr[loseNum] - df.TOW[i] + df.TOL[i]

    cumu = cumDf
    target = cumu.ptDiff

#Max Mean Normalization
#standard_scaler = preprocessing.StandardScaler()
#scaled = standard_scaler.fit_transform(data)
#scaled = pd.DataFrame(scaled, columns=cumu.columns)
#scaled.drop(['week'],axis = 1 , inplace = True)

    cumu.drop(['ptDiff'],axis = 1 , inplace = True)

    NN_model = Sequential()

# The Input Layer :
#NN_model.add(Dropout(0.2, input_shape=(data.shape[1],)))
    NN_model.add(Dense(128, kernel_initializer='normal',input_dim = cumu.shape[1], activation='relu'))
#NN_model.add(Dense(128, kernel_initializer='normal', activation='relu'))

# The Hidden Layers :
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))

# The Output Layer :
    NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

# Compile and Fit the network (Already Done):
#NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
#NN_model.summary()

#checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5'
#checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, mode ='auto')
#callbacks_list = [checkpoint]
#NN_model.fit(data, target, epochs=500, batch_size=32, validation_split = 0.2, callbacks=callbacks_list)
    weights_file = "Weights-499--8.15582.hdf5"
    NN_model.load_weights(weights_file)
    NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])

    winNum = hashC(str1)
    loseNum = hashC(str2)
    row = pd.DataFrame([[21,
            winArr[winNum] - winArr[loseNum],
            ptsArr[winNum] - ptsArr[loseNum],
            ydsArr[winNum] - ydsArr[loseNum],
            toArr[winNum] - toArr[loseNum]]],
            columns = ['week', 'recordDiff', 'cumPtDiffDiff', 'cumYdsDiff', 'cumToDiff'])
    pred = NN_model.predict(row)
    return pred[0][0]

def hashC(name):
    df = pd.read_excel("nfldata.xlsx")
    i = 0
    for x in df.win[0:16]:
        if x == name:
            return i
        else:
            i = i + 1
    for x in df.lose[0:16]:
        if x == name:
            return i
        i = i + 1
