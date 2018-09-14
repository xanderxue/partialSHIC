import keras
import os
import numpy as np
from sklearn import metrics
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

selVals={"Neutral":0,"Hard":1,"Soft":2,"HardPartial":3,"SoftPartial":4}
def getSelType(x):
  if "Neut" in x:
    return "Neutral"
  elif "PartialHard" in x:
    return "HardPartial"
  elif "PartialSoft" in x:
    return "SoftPartial"
  elif "Hard" in x:
    return "Hard"
  elif "Soft" in x:
    return "Soft"
  else:
    raise ValueError

for i in ['AOM','BFM','BFS','CMS','GAS','GNS','GWA','UGS']:
  netlayers=keras.models.load_model('roc/training_sims_2.3.1/'+i+'/training_binary_selection.npy')
  testX={}
  for testSetFileName in os.listdir('FVs_SAFE_stats_no_nSL/'+i):
    testSetFile=open('FVs_SAFE_stats_no_nSL/'+i+'/'+testSetFileName)
    currTestData=testSetFile.readlines()
    testSetFile.close()
    currTestData=currTestData[1:]
    testX[testSetFileName]=[]
    for testExample in currTestData:
      if not "nan" in testExample:
        testData=testExample.strip().split("\t")
        currVector=[]
        for j in range(len(testData)):
          currVector.append(float(testData[j]))
        testX[testSetFileName].append(currVector)
    testX[testSetFileName]=np.reshape(np.array(testX[testSetFileName]),(np.array(testX[testSetFileName]).shape[0],89,11,1))
  true_models=[]
  scores=[]
  for testSetFileName in sorted(testX, key=lambda x: (selVals[getSelType(x)], int((x.split(".")[0]+"_0").split("_")[1]))):
    if int((testSetFileName.split(".")[0]+"_0").split("_")[1])==5:
      true_models.append(np.repeat(1,len(testX[testSetFileName])))
    else:
      true_models.append(np.repeat(0,len(testX[testSetFileName])))
    scores.append(netlayers.predict(testX[testSetFileName])[:,1])
  thresholds=[]
  fpr,tpr,threshold = metrics.roc_curve(np.concatenate(true_models),np.concatenate(scores))
  thresholds.append(threshold)
  auc=metrics.auc(fpr,tpr)
  fig=plt.figure()
  plt.plot(fpr,tpr,color='green',lw=2,label='ROC curve for partialS/HIC (AUC = %0.3f)' %auc)
  for j in range(3):
    scores=[]
    for k in sorted(testX, key=lambda x: (selVals[getSelType(x)], int((x.split(".")[0]+"_0").split("_")[1]))):
      for l in range(len(testX[k])):
        scores.append(testX[k][l][[11,12,13][j]][5])
    fpr,tpr,threshold = metrics.roc_curve(np.concatenate(true_models),scores)
    thresholds.append(threshold)
    auc=metrics.auc(fpr,tpr)
    plt.plot(fpr,tpr,color=['blue','red','orange'][j],lw=2,label='ROC curve for %s (AUC = %0.3f)' %(['E[iHS]','maximum iHS','proportion of iHS outliers'][j],auc))
  plt.plot([0,1],[0,1],'k--',lw=2)
  plt.xlim([0.0,1.0])
  plt.ylim([0.0,1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.legend(loc="lower right",fontsize=7)
  plt.savefig(('roc/'+i+'.roc.pdf'),bbox_inches='tight',dpi=600)
  fileName=open(('roc/'+i+'.thresholds.txt'),'w')
  fileName.write(str(thresholds))
  fileName.close()
