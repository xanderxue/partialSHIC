import sys,os,random

'''usage eg:
python sample_FVs.py spNeut.fvec spHard_ spSoft_ spPartialHard_ spPartialSoft_ 5 0,1,2,3,4,6,7,8,9,10 AOM/ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec
'''

if len(sys.argv)!=10:
  sys.exit("usage:\npython sample_FVs.py neutTrainingFileName hardTrainingFilesPrefix softTrainingFilesPrefix partialHardTrainingFilesPrefix partialSoftTrainingFilesPrefix sweepTrainingWindow linkedTrainingWindows sampledFVsDir sampledFVsFiles\n")
else:
  neutTrainingFileName, hardTrainingFilesPrefix, softTrainingFilesPrefix, partialHardTrainingFilesPrefix, partialSoftTrainingFilesPrefix, sweepTrainingWindow, linkedTrainingWindows, sampledFVsDir, sampledFVsFiles = sys.argv[1:]

sweepFilePaths,linkedFilePaths = {},{}
for trainingFilePrefix in [hardTrainingFilesPrefix,softTrainingFilesPrefix,partialHardTrainingFilesPrefix,partialSoftTrainingFilesPrefix]:
  trainingSetDir="/".join(trainingFilePrefix.split("/")[:-1])
  trainingFilePrefixDirless=trainingFilePrefix.split("/")[-1]
  sweepFilePaths[trainingFilePrefix]=[]
  linkedFilePaths[trainingFilePrefix]=[]
  for fileName in os.listdir(trainingSetDir):
    if fileName.startswith(trainingFilePrefixDirless):
      winNum=int(fileName.split("_")[1].split(".")[0])
      if winNum==int(sweepTrainingWindow):
        sweepFilePaths[trainingFilePrefix].append(trainingSetDir+"/"+fileName)
      elif winNum in [int(x) for x in linkedTrainingWindows.split(",")]:
        linkedFilePaths[trainingFilePrefix].append(trainingSetDir+"/"+fileName)

def getExamplesFromFVFile(simFileName):
  try:
    simFile=open(simFileName)
    lines=[line.strip() for line in simFile.readlines()]
    header=lines[0]
    examples=lines[1:]
    simFile.close()
    return header,examples
  except Exception:
    return "",[]

def getExamplesFromFVFileLs(simFileLs):
  examples=[]
  keptHeader=""
  for filePath in simFileLs:
    header,currExamples=getExamplesFromFVFile(filePath)
    if header:
      keptHeader=header
    examples+=currExamples
  return keptHeader,examples

header,neutExamples=getExamplesFromFVFile(neutTrainingFileName)
hardHeader,hardExamples=getExamplesFromFVFileLs(sweepFilePaths[hardTrainingFilesPrefix])
linkedHardHeader,linkedHardExamples=getExamplesFromFVFileLs(linkedFilePaths[hardTrainingFilesPrefix])
softHeader,softExamples=getExamplesFromFVFileLs(sweepFilePaths[softTrainingFilesPrefix])
linkedSoftHeader,linkedSoftExamples=getExamplesFromFVFileLs(linkedFilePaths[softTrainingFilesPrefix])
partialHardHeader,partialHardExamples=getExamplesFromFVFileLs(sweepFilePaths[partialHardTrainingFilesPrefix])
linkedPartialHardHeader,linkedPartialHardExamples=getExamplesFromFVFileLs(linkedFilePaths[partialHardTrainingFilesPrefix])
partialSoftHeader,partialSoftExamples=getExamplesFromFVFileLs(sweepFilePaths[partialSoftTrainingFilesPrefix])
linkedPartialSoftHeader,linkedPartialSoftExamples=getExamplesFromFVFileLs(linkedFilePaths[partialSoftTrainingFilesPrefix])

def getMinButNonZeroExamples(lsLs):
  counts=[]
  for ls in lsLs:
    if len(ls)>0:
      counts.append(len(ls))
  if not counts:
    raise Exception
  return min(counts)

trainingSetLs=[hardExamples,linkedHardExamples,softExamples,linkedSoftExamples,partialHardExamples,linkedPartialHardExamples,partialSoftExamples,linkedPartialSoftExamples]
numExamplesToKeep=getMinButNonZeroExamples(trainingSetLs)
for i in range(len(trainingSetLs)):
  random.shuffle(trainingSetLs[i])
  trainingSetLs[i]=trainingSetLs[i][:numExamplesToKeep]
hardExamples,linkedHardExamples,softExamples,linkedSoftExamples,partialHardExamples,linkedPartialHardExamples,partialSoftExamples,linkedPartialSoftExamples=trainingSetLs

if sampledFVsDir.lower() in ["none","false","default"]:
  sampledFVsDir='./'
if sampledFVsFiles.lower() in ["none","false","default"]:
  sampledFVsFiles=["neut.fvec","hard.fvec","linkedHard.fvec","soft.fvec","linkedSoft.fvec","partialHard.fvec","linkedPartialHard.fvec","partialSoft.fvec","linkedPartialSoft.fvec"]
else:
  sampledFVsFiles=sampledFVsFiles.split(",")
  assert len(sampledFVsFiles)==9
outExamples=[neutExamples,hardExamples,linkedHardExamples,softExamples,linkedSoftExamples,partialHardExamples,linkedPartialHardExamples,partialSoftExamples,linkedPartialSoftExamples]
for i in range(len(sampledFVsFiles)):
  if outExamples[i]:
    outFile=open('/'.join((sampledFVsDir+'/'+sampledFVsFiles[i]).split('//')),"w")
    outFile.write("classLabel\t%s\n" %(hardHeader))
    for example in outExamples[i]:
      outFile.write("%s\t%s\n" %(sampledFVsFiles[i].replace(".fvec",""),example))
    outFile.close()
