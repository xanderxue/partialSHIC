#source activate python3
import time
startTime=time.clock()
import sys,os
import keras
import numpy as np
from sklearn import metrics
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

'''usage eg:
python test_classifier.py AOM/training.npy FVs/AOM/ 11 92 AOM/ accuracy thresholds.txt confusion_matrix.pdf roc_curve.pdf
'''

if len(sys.argv)!=10:
  sys.exit("usage:\npython test_classifier.py classifierPickleFileName fvecDir numSubWins numSumStatsPerSubWin resultsDir accuracyFilesPrefix thresholdsFileName confusionMatrixFigFileName rocCurveFigFileName\n")
else:
  classifierPickleFileName, fvecDir, numSubWins, numSumStatsPerSubWin, resultsDir, accuracyFilesPrefix, thresholdsFileName, confusionMatrixFigFileName, rocCurveFigFileName = sys.argv[1:]

netlayers=keras.models.load_model(classifierPickleFileName)
if fvecDir.lower() in ["none","false","default"]:
  fvecDir='./'
testX={}
numSubWins=int(numSubWins)
for testSetFileName in os.listdir(fvecDir):
  testSetFile=open('/'.join((fvecDir+'/'+testSetFileName).split('//')))
  currTestData=testSetFile.readlines()
  testSetFile.close()
  currTestData=currTestData[1:]
  testX[testSetFileName]=[]
  for testExample in currTestData:
    if not "nan" in testExample:
      testData=testExample.strip().split("\t")
      currVector=[]
      for i in range(len(testData)):
        currVector.append(float(testData[i]))
      testX[testSetFileName].append(currVector)
  testX[testSetFileName]=np.reshape(np.array(testX[testSetFileName]),(np.array(testX[testSetFileName]).shape[0],int(numSumStatsPerSubWin),numSubWins,1))

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
true_models=[]
scores=[]
classOrder="Neutral Selection".split()
labelToClassName={0:"Neutral",1:"Selection"}
outlinesH={}
accuracyOverall=0
accuracySpecific=0
accuracyBroad=0
for testSetFileName in sorted(testX, key=lambda x: (selVals[getSelType(x)], int((x.split(".")[0]+"_0").split("_")[1]))):
  if int((testSetFileName.split(".")[0]+"_0").split("_")[1])==5:
    true_models.append(np.repeat(1,len(testX[testSetFileName])))
  else:
    true_models.append(np.repeat(0,len(testX[testSetFileName])))
  predictions=np.argmax(netlayers.predict(testX[testSetFileName]),axis=1)
  scores.append(netlayers.predict(testX[testSetFileName])[:,1])
  currPreds={}
  for className in classOrder:
    currPreds[className]=0
  denom=float(len(testX[testSetFileName]))
  for testExampleIndex in range(len(predictions)):
    predictedClass=labelToClassName[predictions[testExampleIndex]]
    currPreds[predictedClass]+=1/denom
  if not testSetFileName=='spNeut.fvec':
    testSetFilePrefix=testSetFileName.split(".")[0].split("_")
    selType,selWin = getSelType(testSetFilePrefix[0]),testSetFilePrefix[1]
    selWin=int(selWin)
    key=(selType,selWin)
  else:
    key=('Neutral',0)
  outlinesH[key]=(testSetFileName,[currPreds[className] for className in classOrder])
  if key[0]=='Neutral' or key[1]!=5:
    accuracyOverall+=currPreds["Neutral"]
    if key[0]=='Neutral':
      accuracySpecific+=currPreds["Neutral"]
      accuracyBroad+=currPreds["Neutral"]
    else:
      accuracyBroad+=currPreds["Selection"]
  else:
    accuracyOverall+=currPreds["Selection"]
    accuracyBroad+=currPreds["Selection"]
  if key[1]==5:
    accuracySpecific+=currPreds["Selection"]

if resultsDir.lower() in ["none","false","default"]:
  resultsDir='./'
if accuracyFilesPrefix.lower() in ["none","false","default"]:
  accuracyFilesPrefix='accuracy'
accuracyOverall=accuracyOverall/((4*numSubWins)+1)
fileName=open('/'.join((resultsDir+'/'+accuracyFilesPrefix+'_overall.txt').split('//')),'w')
fileName.write(str(accuracyOverall))
fileName.close()
accuracySpecific=accuracySpecific/5
fileName=open('/'.join((resultsDir+'/'+accuracyFilesPrefix+'_specific.txt').split('//')),'w')
fileName.write(str(accuracySpecific))
fileName.close()
accuracyBroad=accuracyBroad/((4*numSubWins)+1)
fileName=open('/'.join((resultsDir+'/'+accuracyFilesPrefix+'_broad.txt').split('//')),'w')
fileName.write(str(accuracyBroad))
fileName.close()
fpr,tpr,thresholds = metrics.roc_curve(np.concatenate(true_models),np.concatenate(scores))
auc=metrics.auc(fpr,tpr)
fileName=open('/'.join((resultsDir+'/'+thresholdsFileName).split('//')),'w')
fileName.write(str(thresholds))
fileName.close()


fig=plt.figure()
rowLabels,data = [],[]
for selType in sorted(selVals, key=lambda x: selVals[x]):
 for selWin in range(numSubWins):
  if selType!="Neutral" or selWin==0:
    if "Neutral" in selType:
      rowLabels.append("Neutral")
    else:
      if selWin==5:
        rowLabels.append("%s sweep in focal window" %selType)
      else:
        diff=abs(selWin-5)
        if diff==1:
          plural=""
        else:
          plural="s"
        if selWin<5:
          direction="left"
        else:
          direction="right"
        rowLabels.append("%s sweep %s window%s to %s" %(selType, diff, plural, direction))
    vec=outlinesH[(selType,selWin)][1]
    data.append(vec)
data=np.array(data)
ax=plt.subplots()[1]
heatmap=ax.pcolor(data,cmap=plt.cm.Blues,vmin=0.0,vmax=1.0)
cbar=plt.colorbar(heatmap,cmap=plt.cm.Blues)
cbar.set_label('Fraction of simulations assigned to class',rotation=270,labelpad=20)
ax.set_xticks(np.arange(data.shape[1])+0.5,minor=False)
ax.set_yticks(np.arange(data.shape[0])+0.5,minor=False)
ax.invert_yaxis()
ax.xaxis.tick_top()
ax.axis('tight')
plt.tick_params(axis='y',which='both',right='off')
plt.tick_params(axis='x',which='both',direction='out')
ax.set_xticklabels(classOrder,minor=False,fontsize=9,rotation=45,ha="left")
ax.set_yticklabels(rowLabels,minor=False,fontsize=7)
for y in range(data.shape[0]):
  for x in range(data.shape[1]):
    val=data[y,x]
    val*=100
    if val>50:
      c='0.9'
    else:
      c='black'
    ax.text(x+0.5,y +0.5,'%.1f%%' % val,horizontalalignment='center',verticalalignment='center',color=c,fontsize=6)
if confusionMatrixFigFileName.lower() in ["none","false","default"]:
  confusionMatrixFigFileName='confusionmatrix.pdf'
plt.savefig('/'.join((resultsDir+'/'+confusionMatrixFigFileName).split('//')),bbox_inches='tight',dpi=600)

fig=plt.figure()
plt.plot(fpr,tpr,color='green',lw=2,label='ROC curve for deep learning (AUC = %0.3f)' %auc)
thresholds=[]
for j in range(2):
  scores=[]
  for k in sorted(testX, key=lambda x: (selVals[getSelType(x)], int((x.split(".")[0]+"_0").split("_")[1]))):
    for l in range(len(testX[k])):
      scores.append(testX[k][l][[11,12][j]][5])
  fprX,tprX,threshold = metrics.roc_curve(np.concatenate(true_models),scores)
  thresholds.append(threshold)
  aucX=metrics.auc(fprX,tprX)
  plt.plot(fprX,tprX,color=['blue','red'][j],lw=2,label='ROC curve for %s (AUC = %0.3f)' %(['iHSMean','iHSMax'][j],aucX))
plt.plot([0,1],[0,1],'k--',lw=2)
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curves for binary classification of focal window selective sweep')
plt.legend(loc="lower right",fontsize=7)
plt.savefig('/'.join((resultsDir+'/'+rocCurveFigFileName).split('//')),bbox_inches='tight',dpi=600)
fileName=open((resultsDir+'/'+rocCurveFigFileName.replace('.pdf','')+'.iHS_nSL_thresholds'),'w')
fileName.write(str(thresholds))
fileName.close()

sys.stderr.write("total time spent testing classifier stored in %s on feature vector sets in %s: %f secs\n" %(classifierPickleFileName,fvecDir,(time.clock()-startTime)))
