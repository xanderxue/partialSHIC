import time
startTime=time.clock()
import sys
import numpy as np
np.random.seed(123)
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Activation,Dropout,Flatten,Dense
from keras import optimizers
from keras.callbacks import EarlyStopping,ModelCheckpoint

'''usage eg:
python3 training_deep_learning.py ./ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec 11 89 0.1 training_weights.hdf5 training.json training.npy
'''

if len(sys.argv)!=9:
  sys.exit("usage:\npython3 training_deep_learning.py fvecDir fvecFiles numSubWins numSumStatsPerSubWin validationSize weightsFileName jsonFileName npyFileName\n")
else:
  fvecDir, fvecFiles, numSubWins, numSumStatsPerSubWin, validationSize, weightsFileName, jsonFileName, npyFileName = sys.argv[1:]

if fvecDir.lower() in ["none","false","default"]:
  fvecDir='./'
if fvecFiles.lower() in ["none","false","default"]:
  fvecFiles=['neut.fvec','hard.fvec','linkedHard.fvec','soft.fvec','linkedSoft.fvec','partialHard.fvec','linkedPartialHard.fvec','partialSoft.fvec','linkedPartialSoft.fvec']
else:
  fvecFiles=fvecFiles.split(",")
  assert len(fvecFiles)==9
numSubWins,numSumStatsPerSubWin = int(numSubWins),int(numSumStatsPerSubWin)
if validationSize.lower() in ["none","false","default"]:
  validationSize=0.1
else:
  validationSize=float(validationSize)

sweeps=[]
for i in range(0,9):
 sweeps.append(np.loadtxt('/'.join((fvecDir+'/'+fvecFiles[i]).split('//')),skiprows=1,usecols=list(range(1,((numSubWins*numSumStatsPerSubWin)+1)))))
 if i>0:
  assert len(sweeps[0])==len(sweeps[i])
sumstats=np.concatenate((sweeps[0],sweeps[1],sweeps[2],sweeps[3],sweeps[4],sweeps[5],sweeps[6],sweeps[7],sweeps[8]))
sumstats=sumstats.reshape(sumstats.shape[0],numSumStatsPerSubWin,numSubWins,1)
models=np.concatenate((np.repeat(0,len(sweeps[0])),np.repeat(1,len(sweeps[0])),np.repeat(2,len(sweeps[0])),np.repeat(3,len(sweeps[0])),np.repeat(4,len(sweeps[0])),np.repeat(5,len(sweeps[0])),np.repeat(6,len(sweeps[0])),np.repeat(7,len(sweeps[0])),np.repeat(8,len(sweeps[0]))))
sumstats,sumstats_val,models,models_val = train_test_split(sumstats,models,test_size=validationSize,random_state=42)
models=np_utils.to_categorical(models,9)
models_val=np_utils.to_categorical(models_val,9)

netlayers=Sequential()
netlayers.add(Conv2D(256,(3, 6),padding='same',input_shape=sumstats.shape[1:]))
netlayers.add(MaxPooling2D(pool_size=(3,3),padding='same'))
netlayers.add(Conv2D(256,(3, 3),padding='same',activation='relu'))
netlayers.add(MaxPooling2D(pool_size=(3,3),padding='same'))
netlayers.add(Dropout(0.25))
netlayers.add(Flatten())
netlayers.add(Dense(512, activation='relu'))
netlayers.add(Dropout(0.5))
netlayers.add(Dense(128, activation='relu'))
netlayers.add(Dropout(0.5))
netlayers.add(Dense(9, activation='softmax'))
netlayers.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

checkpoint=ModelCheckpoint(weightsFileName,monitor='val_acc',verbose=1,save_best_only=True,save_weights_only=True,mode='auto')
netlayers.fit(sumstats,models,batch_size=32,epochs=20,validation_data=(sumstats_val,models_val),callbacks=[checkpoint],verbose=1)

netlayers_json=netlayers.to_json()
with open(jsonFileName,"w") as json_file:
  json_file.write(netlayers_json)
netlayers.save(npyFileName)
sys.stderr.write("total time spent fitting and validating convolutional neural network for deep learning: %f secs\n" %(time.clock()-startTime))

