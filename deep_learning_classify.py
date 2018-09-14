#source activate python3
import time
startTime=time.clock()
import sys
import keras
import numpy as np

'''usage eg:
python deep_learning_classify.py AOM/training.npy data/FVs/AOM.2L.fvec 11 92 results/AOM.2L.bed
'''

if len(sys.argv)!=6:
  sys.exit("usage:\npython deep_learning_classify.py classifierPickleFileName fvecFileName numSubWins numSumStatsPerSubWin bedFileName\n")
else:
  classifierPickleFileName, fvecFileName, numSubWins, numSumStatsPerSubWin, bedFileName = sys.argv[1:]

netlayers=keras.models.load_model(classifierPickleFileName)
fvecFile=open(fvecFileName)
fvec=fvecFile.readlines()
fvecFile.close()
fvec=fvec[1:]
coords,fvecData=[],[]
numSubWins,numSumStatsPerSubWin = int(numSubWins),int(numSumStatsPerSubWin)
for example in fvec:
  if not "nan" in example:
    coords.append(example.strip().split("\t")[:-(numSubWins*numSumStatsPerSubWin)])
    exampleData=example.strip().split("\t")[-(numSubWins*numSumStatsPerSubWin):]
    currVector=[]
    for i in range(len(exampleData)):
      currVector.append(float(exampleData[i]))
    fvecData.append(currVector)
if not fvecData:
  sys.exit("Weird: no nan-less features in input file. Terminating...\n")
fvecData=np.reshape(np.array(fvecData),(np.array(fvecData).shape[0],numSumStatsPerSubWin,numSubWins,1))
predictions=np.argmax(netlayers.predict(fvecData),axis=1)
labelToClassName={0:"Neutral",1:"Hard",2:"Hard-linked",3:"Soft",4:"Soft-linked",5:"HardPartial",6:"HardPartial-linked",7:"SoftPartial",8:"SoftPartial-linked"}
predictionCounts={}
for i in range(9):
  predictionCounts[labelToClassName[i]]=0
outlines=["track name=sweep_classifications description=\"Classification from sweeps inference tool\" visibility=2 itemRgb=On"]
classToColorStr={"Neutral": "0,0,0", "Hard":"255,0,0", "Hard-linked":"255,150,150", "Soft":"0,0,255", "Soft-linked":"150,150,255", "HardPartial":"255,120,0", "HardPartial-linked":"255,200,100", "SoftPartial":"175,0,255", "SoftPartial-linked":"200,120,230"}
if bedFileName.lower() in ["none","false","default"]:
  bedFileName=fvecFileName.split('/')[-1].replace(".fvec","")+".bed"
bedFile=open(bedFileName,"w")
for i in range(len(predictions)):
  chr,start,end=coords[i][:3]
  start,end = int(start),int(end)
  predictedClass=labelToClassName[predictions[i]]
  predictionCounts[predictedClass]+=1
  outlines.append("chr%s\t%d\t%d\t%s_%s_%s\t0\t.\t%d\t%d\t%s" %(chr, (start-1), end, predictedClass, chr, predictionCounts[predictedClass], (start-1), end, classToColorStr[predictedClass]))
  bedFile.write(outlines[i]+"\n")
bedFile.close()

sys.stderr.write("made predictions for %s total instances\n" %len(predictions))
sys.stderr.write("predicted %d neutral regions (%f of all classified regions)\n" %(predictionCounts["Neutral"],(predictionCounts["Neutral"]/float(len(predictions)))))
for i in range(1,9):
  sys.stderr.write("predicted %d %s sweep regions (%f of all classified regions)\n" %(predictionCounts[labelToClassName[i]],labelToClassName[i],(predictionCounts[labelToClassName[i]]/float(len(predictions)))))
sys.stderr.write("total time spent classifying data in %s with convolutional neural network stored in %s : %f secs\n" %(fvecFileName,classifierPickleFileName,(time.clock()-startTime)))
