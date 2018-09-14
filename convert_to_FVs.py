#HAF/phi/kappa/SFS/SAFE distribution stats
import time
startTime=time.clock()
import sys
from msTools import *
from fvTools import *
import random
import allel
import numpy as np
import math

'''usage eg:
pMisPol=`python /san/personal/dan/ag1kg/demogInferenceStuff/stairwayPlotToPMisPol.py /san/personal/dan/ag1kg/demogInferenceStuff/spSummaryOutput/AOM.meru_mela.sfs.sp.summary`
python convert_to_FVs.py spNeut.msOut.gz 2L,2R,3L,3R 5000 11 0.25 $pMisPol /san/personal/dan/ag1kg/shicScanPhaseI/partialStatsAndDafs/AOM_partial_stats.txt /san/data/ag1kg/accessibility/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa /san/data/ag1kg/outgroups/anc.meru_mela.fa sumstats/AOM/ FVs/AOM/spNeut.msOut.fvec
'''

if len(sys.argv)!=12:
  sys.exit("usage:\npython convert_to_FVs.py trainingDataFileName chrArmsForMasking subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName statDir fvecFileName\n")
else:
  trainingDataFileName, chrArmsForMasking, subWinSize, numSubWins, unmaskedFracCutoff, pMisPol, partialStatAndDafFileName, maskFileName, ancestralArmFaFileName, statDir, fvecFileName = sys.argv[1:]

subWinSize,numSubWins = int(subWinSize),int(numSubWins)
assert subWinSize>0 and numSubWins>1
totalPhysLen=(subWinSize*numSubWins)
trainingDataFileObj,sampleSize,numInstances=openMsOutFileForSequentialReading(trainingDataFileName)
chrArmsForMasking=chrArmsForMasking.split(",")
unmaskedFracCutoff,pMisPol=float(unmaskedFracCutoff),float(pMisPol)
if unmaskedFracCutoff>1.0:
  sys.exit("unmaskedFracCutoff must lie within [0, 1].\n")
if pMisPol>1.0:
  sys.exit("pMisPol must lie within [0, 1].\n")
standardizationInfo=readStatsDafsComputeStandardizationBins(partialStatAndDafFileName,nBins=50,pMisPol=pMisPol)
if maskFileName.lower() in ["none", "false"]:
  unmaskedFracCutoff=1.0
  unmasked=[True]*totalPhysLen
  sys.stderr.write("Warning: not doing any masking! (i.e. mask.fa file for the chr arm with all masked sites N'ed out, or at least the reference with Ns, is not provided)\n")
  maskFileName=False
else:
  if ancestralArmFaFileName.lower() in ["none", "false"]:
    maskData=readMaskDataForTraining(maskFileName,totalPhysLen,subWinSize,chrArmsForMasking,shuffle=True,cutoff=unmaskedFracCutoff)
  else:
    maskData=readMaskAndAncDataForTraining(maskFileName,ancestralArmFaFileName,totalPhysLen,subWinSize,chrArmsForMasking,shuffle=True,cutoff=unmaskedFracCutoff)
  if len(maskData)<numInstances:
    sys.stderr.write("Warning: not enough windows from masked data (needed %d; got %d); will draw with replacement!!\n" %(numInstances,len(maskData)))
    drawWithReplacement=True
  else:
    sys.stderr.write("enough windows from masked data (needed %d; got %d); will draw without replacement.\n" %(numInstances,len(maskData)))
    drawWithReplacement=False

statNames=["pi", "thetaW", "tajD", "thetaH", "fayWuH", "HapCount", "H1", "H12", "H2/H1", "ZnS", "Omega", "iHSMean", "iHSMax", "iHSOutFrac", "nSLMean", "nSLMax", "nSLOutFrac", "distVar", "distSkew", "distKurt"]
for i in ["HAF", "HAFunique", "phi", "kappa", "SFS", "SAFE"]:
  for j in ["Mean", "Median", "Mode", "Lower95%", "Lower50%", "Upper50%", "Upper95%", "Max", "Var", "SD", "Skew", "Kurt"]:
    statNames.append("%s-%s" %(i, j))
header=[]
for statName in statNames:
  for i in range(numSubWins):
    header.append("%s_win%d" %(statName, i))
header="\t".join(header)

statVals={}
for statName in statNames:
  statVals[statName]=[]
def getSubWinBounds(subWinSize,totalPhysLen):
  subWinStart=1-subWinSize
  subWinEnd=0
  subWinBounds=[]
  for i in range(0,(numSubWins-1)):
    subWinStart+=subWinSize
    subWinEnd+=subWinSize
    subWinBounds.append((subWinStart,subWinEnd))
  subWinStart+=subWinSize
  subWinEnd=totalPhysLen
  subWinBounds.append((subWinStart,subWinEnd))
  return subWinBounds
subWinBounds=getSubWinBounds(subWinSize,totalPhysLen)
def getSnpIndicesInSubWins(subWinBounds,positions):
  snpIndicesInSubWins=[]
  for subWinIndex in range(len(subWinBounds)):
    snpIndicesInSubWins.append([])
  subWinIndex=0
  for i in range(len(positions)):
    while not (positions[i]>=subWinBounds[subWinIndex][0] and positions[i]<=subWinBounds[subWinIndex][1]):
      subWinIndex+=1
    snpIndicesInSubWins[subWinIndex].append(i)
  return snpIndicesInSubWins
quantiles={"Lower95%":2.5,"Lower50%":25,"Upper50%":75,"Upper95%":97.5}
if statDir.lower() in ["none","false","default"]:
  statDir='./'
statFiles=[]
for subWinIndex in range(numSubWins):
  statFileName='/'.join(("%s/%s.subWin%d.stats" %(statDir, trainingDataFileName.split("/")[-1].replace(".msOut.gz",""), subWinIndex)).split('//'))
  statFiles.append(open(statFileName,"w"))
  statFiles[-1].write("\t".join(statNames)+"\n")
if fvecFileName.lower() in ["none","false","default"]:
  fvecFileName="%s.fvec" %trainingDataFileName.split("/")[-1].replace(".msOut.gz","")
fvecFile=open(fvecFileName,"w")
fvecFile.write(header+"\n")

for instanceIndex in range(numInstances):
  hapArrayIn,positionArray=readNextMsRepToHaplotypeArrayIn(trainingDataFileObj,sampleSize,totalPhysLen)
  for statName in statNames:
    statVals[statName].append([])
  if maskFileName:
    if drawWithReplacement:
      unmasked=random.choice(maskData)
    else:
      unmasked=maskData[instanceIndex]
    assert len(unmasked)==totalPhysLen
  snpIndicesToKeep=[x for x in range(len(positionArray)) if unmasked[positionArray[x]-1]]
  if len(snpIndicesToKeep)==0:
    for subWinIndex in range(numSubWins):
      for statName in statNames:
        appendStatValsForMonomorphic(statName,statVals,instanceIndex,subWinIndex)
      statFiles[subWinIndex].write("\t".join([str(statVals[statName][instanceIndex][subWinIndex]) for statName in statNames])+"\n")
  else:
    haps=allel.HaplotypeArray(hapArrayIn,dtype='i1').subset(sel0=snpIndicesToKeep)
    if pMisPol>0:
      misPolarizeCorrectionIndex=np.random.binomial(1,pMisPol,len(haps))
      for i in range(len(misPolarizeCorrectionIndex)):
        if misPolarizeCorrectionIndex[i]==1:
          for j in range(len(haps[i])):
            if haps[i][j]==0:
              haps[i][j]=1
            else:
              haps[i][j]=0
    genos=haps.to_genotypes(ploidy=2)
    alleleCounts=genos.count_alleles()
    positions=[positionArray[x] for x in snpIndicesToKeep]
    precomputedStats={}
    dafs=alleleCounts[:,1]/float(sampleSize)
    ihsVals=allel.stats.selection.ihs(haps,positions,use_threads=False,include_edges=False)
    nonNanCount=[x for x in np.isnan(ihsVals)].count(False)
    nonInfCount=[x for x in np.isinf(ihsVals)].count(False)
    sys.stderr.write("number of iHS scores: %d (%d non-nan; %d non-inf)\n" %(len(ihsVals),nonNanCount,nonInfCount))
    if nonNanCount==0:
      precomputedStats["iHS"]=[]
      for subWinIndex in range(numSubWins):
        precomputedStats["iHS"].append([])
    else:
      ihsVals=standardize_by_allele_count_from_precomp_bins(ihsVals,dafs,standardizationInfo["iHS"])
      precomputedStats["iHS"]=windowVals(ihsVals,subWinBounds,positions,keepNans=False,absVal=True)
    nslVals=allel.stats.selection.nsl(haps,use_threads=False)
    nonNanCount=[x for x in np.isnan(nslVals)].count(False)
    sys.stderr.write("number of nSL scores: %d (%d non-nan)\n" %(len(nslVals),nonNanCount))
    if nonNanCount==0:
      precomputedStats["nSL"]=[]
      for subWinIndex in range(numSubWins):
        precomputedStats["nSL"].append([])
    else:
      nslVals=standardize_by_allele_count_from_precomp_bins(nslVals,dafs,standardizationInfo["nSL"])
      precomputedStats["nSL"]=windowVals(nslVals,subWinBounds,positions,keepNans=False,absVal=True)
    snpIndicesInSubWins=getSnpIndicesInSubWins(subWinBounds,positions)
    for subWinIndex in range(numSubWins):
      subWinStart,subWinEnd = subWinBounds[subWinIndex]
      unmaskedFrac=unmasked[subWinStart-1:subWinEnd].count(True)/float(subWinSize)
      assert unmaskedFrac>=unmaskedFracCutoff
      if len(snpIndicesInSubWins[subWinIndex])==0:
        for statName in statNames:
          appendStatValsForMonomorphic(statName,statVals,instanceIndex,subWinIndex)
      else:
        hapsInSubWin=haps.subset(sel0=snpIndicesInSubWins[subWinIndex])
        for statName in [x for x in statNames if x[0:3]!="HAF" and x[0:3]!="phi" and x[0:3]!="kap" and x[0:3]!="SFS" and x[0:3]!="SAF"]:
          calcAndAppendStatVal(alleleCounts, positions, statName, subWinStart, subWinEnd, statVals, instanceIndex, subWinIndex, hapsInSubWin, unmasked, precomputedStats)
        haplotypes={}
        for i in range(len(hapsInSubWin[0])):
          haplotype=[hapsInSubWin[x][i] for x in range(len(hapsInSubWin))]
          haplotype="".join(str(x) for x in haplotype)
          if haplotype in haplotypes:
            haplotypes[haplotype].append(i)
          else:
            haplotypes[haplotype]=[i]
        HAF=[]
        HAFunique={}
        for i in haplotypes:
          HAFunique[i]=0
          for j in range(len(hapsInSubWin)):
            if hapsInSubWin[j][haplotypes[i][0]]==1:
              HAFunique[i]+=sum([hapsInSubWin[j][x] for x in range(len(hapsInSubWin[j]))])
          for j in range(len(haplotypes[i])):
            HAF.append(HAFunique[i])
        phi=[]
        kappa=[]
        SAFE=[]
        for i in range(len(hapsInSubWin)):
          phi.append(0)
          kappa.append([])
          phiDenom=0
          for j in haplotypes:
            phi[i]+=(int(list(j)[i])*HAFunique[j]*len(haplotypes[j]))
            if int(list(j)[i])==1 and HAFunique[j] not in kappa[i] and HAFunique[j]!=0:
              kappa[i].append(HAFunique[j])
            phiDenom+=(HAFunique[j]*len(haplotypes[j]))
          phi[i]/=float(phiDenom)
          kappa[i]=len(kappa[i])/float(len(set([HAFunique[x] for x in HAFunique if HAFunique[x]!=0])))
          if dafs[snpIndicesInSubWins[subWinIndex]][i]==0 or dafs[snpIndicesInSubWins[subWinIndex]][i]==1:
           SAFE.append(0.0)
          else:
           SAFE.append((phi[i]-kappa[i])/float(math.sqrt(dafs[snpIndicesInSubWins[subWinIndex]][i]*(1-dafs[snpIndicesInSubWins[subWinIndex]][i]))))
        for i in ["HAF", "HAFunique", "phi", "kappa", "SFS", "SAFE"]:
          if i=="SFS":
            windowStats=dafs[snpIndicesInSubWins[subWinIndex]]
          elif i=="HAFunique":
            windowStats=[eval(i)[x] for x in eval(i)]
          else:
            windowStats=eval(i)
          statVals[i+"-Mean"][instanceIndex].append(np.mean(windowStats))
          statVals[i+"-Median"][instanceIndex].append(np.median(windowStats))
          if(len(np.unique(windowStats,return_counts=True)[1])==1):
            statVals[i+"-Mode"][instanceIndex].append(windowStats[0])
          else:
            if(sorted(np.unique(windowStats,return_counts=True)[1])[-1]!=sorted(np.unique(windowStats,return_counts=True)[1])[-2]):
              statVals[i+"-Mode"][instanceIndex].append(scipy.stats.mstats.mode(windowStats)[0][0])
            else:
              mode=min(windowStats)
              for j in range(1,51):
                if len([x for x in windowStats if x>=(min(windowStats)+(j*((max(windowStats)-min(windowStats))/50))) and x<(min(windowStats)+((j+1)*((max(windowStats)-min(windowStats))/50)))]) >= len([x for x in windowStats if x>=mode and x<(mode+((max(windowStats)-min(windowStats))/50))]):
                  mode=min(windowStats)+(j*((max(windowStats)-min(windowStats))/50))
              statVals[i+"-Mode"][instanceIndex].append(mode+((max(windowStats)-min(windowStats))/100))
          for j in quantiles:
            statVals[i+"-"+j][instanceIndex].append(np.percentile(windowStats,quantiles[j]))
          statVals[i+"-Max"][instanceIndex].append(max(windowStats))
          statVals[i+"-Var"][instanceIndex].append(np.var(windowStats))
          statVals[i+"-SD"][instanceIndex].append(np.std(windowStats))
          statVals[i+"-Skew"][instanceIndex].append(scipy.stats.skew(windowStats))
          statVals[i+"-Kurt"][instanceIndex].append(scipy.stats.kurtosis(windowStats))
      statFiles[subWinIndex].write("\t".join([str(statVals[statName][instanceIndex][subWinIndex]) for statName in statNames])+"\n")
  outVec=[]
  for statName in statNames:
    outVec+=normalizeFeatureVec(statVals[statName][instanceIndex])
  fvecFile.write("\t".join([str(x) for x in outVec])+"\n")

closeMsOutFile(trainingDataFileObj)
for subWinIndex in range(numSubWins):
  statFiles[subWinIndex].close()
fvecFile.close()
sys.stderr.write("total time spent calculating summary statistics and generating feature vectors: %g secs\n" %(time.clock()-startTime))
