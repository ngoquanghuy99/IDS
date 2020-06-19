from __future__ import print_function
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import LSTM, SimpleRNN, GRU
from keras.datasets import imdb
from keras.utils.np_utils import to_categorical
from sklearn.metrics import (precision_score, recall_score,
                             f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.preprocessing import Normalizer
import h5py
from keras import callbacks
from keras import callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger

#traindata = pd.read_csv('dataset/training.csv', header=None)
testdata = pd.read_csv('dataset/testing.csv', header=None)


#X = traindata.iloc[:,0:42]
#Y = traindata.iloc[:,0]
C = testdata.iloc[:,0]
T = testdata.iloc[:,1:42]

'''
scaler = Normalizer().fit(X)
trainX = scaler.transform(X)
# summarize transformed data
np.set_printoptions(precision=3)
#print(trainX[0:5,:])
'''
scaler = Normalizer().fit(T)
testT = scaler.transform(T)
# summarize transformed data
np.set_printoptions(precision=3)
#print(testT[0:5,:])


#y_train1 = np.array(Y)
y_test1 = np.array(C)

#y_train= to_categorical(y_train1)
y_test= to_categorical(y_test1)



# reshape input to be [samples, time steps, features]
#X_train = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
X_train = np.reshape(testT, (testT.shape[0], 1, testT.shape[1]))


batch_size = 32

# 1. define the network
model = Sequential()
model.add(LSTM(8,input_dim=41, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(LSTM(8,input_dim=41, return_sequences=False))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(Dense(5))
model.add(Activation('softmax'))



# try using different optimizers and different optimizer configs
model.load_weights("results/2layer/checkpoint-37.hdf5")

#model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

y_pred = model.predict_classes(X_train)
np.savetxt('res/expected1.txt', y_test1, fmt='%01d')
np.savetxt('res/predicted1.txt', y_pred, fmt='%01d')

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
loss, accuracy = model.evaluate(X_train, y_test)
print("\nLoss: %.2f, Accuracy: %.2f%%" % (loss, accuracy*100))





