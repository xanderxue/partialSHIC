#HAF/phi/kappa/SFS/SAFE distribution stats
import time
startTime=time.clock()
import sys
import h5py
import allel
from fvTools import *
import numpy as np
import math

'''usage eg:
###optional###
segmentStart=1
segmentEnd=2050000
###END###
pMisPol=`python /san/personal/dan/ag1kg/demogInferenceStuff/stairwayPlotToPMisPol.py /san/personal/dan/ag1kg/demogInferenceStuff/spSummaryOutput/AOM.meru_mela.sfs.sp.summary`
python convert_to_FVs.py /san/data/ag1kg/haplotypes/ag1000g.phase1.ar3.haplotypes.2L.h5 2L 49364325 $segmentStart $segmentEnd 5000 11 0.25 $pMisPol /san/personal/dan/ag1kg/shicScanPhaseI/partialStatsAndDafs/AOM_partial_stats.txt /san/data/ag1kg/accessibility/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa /san/data/ag1kg/outgroups/anc.meru_mela.2L.fa /san/data/ag1kg/samples_pops.txt AOM data/sumstats/AOM/2L.$segmentStart.stats data/FVs/AOM/2L.$segmentStart.fvec
'''

if not len(sys.argv) in [15,17]:
  sys.exit("usage:\npython convert_to_FVs.py chrArmFileName chrArm chrLen [segmentStart segmentEnd] subWinSize numSubWins unmaskedFracCutoff pMisPol partialStatAndDafFileName maskFileName ancestralArmFaFileName sampleToPopFileName targetPop statFileName fvecFileName\n")
if len(sys.argv)==17:
  chrArmFileName, chrArm, chrLen, segmentStart, segmentEnd, subWinSize, numSubWins, unmaskedFracCutoff, pMisPol, partialStatAndDafFileName, maskFileName, ancestralArmFaFileName, sampleToPopFileName, targetPop, statFileName, fvecFileName = sys.argv[1:]
else:
  chrArmFileName, chrArm, chrLen, subWinSize, numSubWins, unmaskedFracCutoff, pMisPol, partialStatAndDafFileName, maskFileName, ancestralArmFaFileName, sampleToPopFileName, targetPop, statFileName, fvecFileName = sys.argv[1:]
  segmentStart=None

chrArmFile=h5py.File(chrArmFileName,"r")
genos=allel.GenotypeChunkedArray(chrArmFile[chrArm]["calldata"]["genotype"])
positions=allel.SortedIndex(chrArmFile["/%s/variants/POS" %(chrArm)][:])
refAlleles=chrArmFile[chrArm]['variants']['REF']
altAlleles=chrArmFile[chrArm]['variants']['ALT']
samples=chrArmFile[chrArm]["samples"]
chrLen=int(chrLen)
assert chrLen>0
if segmentStart!=None:
  segmentStart,segmentEnd = int(segmentStart),int(segmentEnd)
  assert segmentStart>0 and segmentEnd>=segmentStart
  snpIndicesToKeep=[x for x in range(len(positions)) if segmentStart<=positions[x]<=segmentEnd]
  genos=allel.GenotypeArray(genos.subset(sel0=snpIndicesToKeep))
  positions=[positions[x] for x in snpIndicesToKeep]
  refAlleles=[refAlleles[x] for x in snpIndicesToKeep]
  altAlleles=[altAlleles[x] for x in snpIndicesToKeep]
subWinSize,numSubWins,unmaskedFracCutoff,pMisPol = int(subWinSize),int(numSubWins),float(unmaskedFracCutoff),float(pMisPol)
assert subWinSize>0 and numSubWins>1
if unmaskedFracCutoff>1.0:
  sys.exit("unmaskedFracCutoff must lie within [0, 1].\n")
if pMisPol>1.0:
  sys.exit("pMisPol must lie within [0, 1].\n")
standardizationInfo=readStatsDafsComputeStandardizationBins(partialStatAndDafFileName,nBins=50,pMisPol=pMisPol)
if maskFileName.lower() in ["none","false"]:
  unmaskedFracCutoff=1.0
  unmasked=[True]*chrLen
  sys.stderr.write("Warning: a mask.fa file for the chr arm with all masked sites N'ed out is strongly recommended (pass in the reference to remove Ns at the very least)!\n")
else:
  unmasked=readMaskDataForScan(maskFileName,chrArm)
  assert len(unmasked)==chrLen
ancArm=readFaArm(ancestralArmFaFileName).upper()
sys.stderr.write("polarizing SNPs\n")
polTime=time.clock()
mapping,unmasked = polarizeSnps(unmasked,positions,refAlleles,altAlleles,ancArm)
sys.stderr.write("took %s seconds to polarize SNPs\n" %((time.clock()-polTime)))
def readSampleToPopFile(sampleToPopFileName):
  table={}
  with open(sampleToPopFileName) as sampleToPopFile:
    for line in sampleToPopFile:
      sample,pop = line.strip().split()
      table[sample]=pop
  return table
sampleToPop=readSampleToPopFile(sampleToPopFileName)
sampleIndicesToKeep=[x for x in range(len(samples)) if sampleToPop.get(samples[x],"popNotFound!")==targetPop]

genos=genos.subset(sel1=sampleIndicesToKeep)
alleleCounts=genos.count_alleles()
isBiallelic=alleleCounts.is_biallelic()
for i in range(len(isBiallelic)):
  if not isBiallelic[i]:
    unmasked[positions[i]-1]=False
snpIndicesToKeep=[x for x in range(len(positions)) if unmasked[positions[x]-1]]
genos=genos.subset(sel0=snpIndicesToKeep)
haps=genos.to_haplotypes()
alleleCounts=allel.AlleleCountsArray([alleleCounts[x] for x in snpIndicesToKeep])
mapping=[mapping[x] for x in snpIndicesToKeep]
alleleCounts=alleleCounts.map_alleles(mapping)
positions=[positions[x] for x in snpIndicesToKeep]

statNames=["pi", "thetaW", "tajD", "thetaH", "fayWuH", "HapCount", "H1", "H12", "H2/H1", "ZnS", "Omega", "iHSMean", "iHSMax", "iHSOutFrac", "nSLMean", "nSLMax", "nSLOutFrac", "distVar", "distSkew", "distKurt"]
for i in ["HAF", "HAFunique", "phi", "kappa", "SFS", "SAFE"]:
  for j in ["Mean", "Median", "Mode", "Lower95%", "Lower50%", "Upper50%", "Upper95%", "Max", "Var", "SD", "Skew", "Kurt"]:
    statNames.append("%s-%s" %(i, j))
statHeader="chrom start end".split()
header="chrom classifiedWinStart classifiedWinEnd bigWinRange".split()
for statName in statNames:
  statHeader.append(statName)
  for i in range(numSubWins):
    header.append("%s_win%d" %(statName,i))
statHeader="\t".join(statHeader)
header="\t".join(header)

precomputedStats={}
def getSubWinBounds(subWinSize,positions):
  subWinStart=1
  subWinEnd=subWinStart+subWinSize-1
  subWinBounds=[]
  for i in range(len(positions)):
    while not (positions[i]>=subWinStart and positions[i]<=subWinEnd):
      subWinStart+=subWinSize
      subWinEnd+=subWinSize
    if (subWinStart,subWinEnd) not in subWinBounds:
      subWinBounds.append((subWinStart,subWinEnd))
  return subWinBounds
subWinBounds=getSubWinBounds(subWinSize,positions)
dafs=alleleCounts[:,1]/float(len(sampleIndicesToKeep)*2)
ihsVals=allel.stats.selection.ihs(haps,positions,use_threads=False,include_edges=False)
nonNanCount=[x for x in np.isnan(ihsVals)].count(False)
nonInfCount=[x for x in np.isinf(ihsVals)].count(False)
sys.stderr.write("number of iHS scores: %d (%d non-nan; %d non-inf)\n" %(len(ihsVals),nonNanCount,nonInfCount))
if nonNanCount==0:
  precomputedStats["iHS"]=[]
  for subWinIndex in range(len(subWinBounds)):
    precomputedStats["iHS"].append([])
else:
  ihsVals=standardize_by_allele_count_from_precomp_bins(ihsVals,dafs,standardizationInfo["iHS"])
  precomputedStats["iHS"]=windowVals(ihsVals,subWinBounds,positions,keepNans=False,absVal=True)
nslVals=allel.stats.selection.nsl(haps,use_threads=False)
nonNanCount=[x for x in np.isnan(nslVals)].count(False)
sys.stderr.write("number of nSL scores: %d (%d non-nan)\n" %(len(nslVals),nonNanCount))
if nonNanCount==0:
  precomputedStats["nSL"]=[]
  for subWinIndex in range(len(subWinBounds)):
    precomputedStats["nSL"].append([])
else:
  nslVals=standardize_by_allele_count_from_precomp_bins(nslVals,dafs,standardizationInfo["nSL"])
  precomputedStats["nSL"]=windowVals(nslVals,subWinBounds,positions,keepNans=False,absVal=True)

#mispolarization information not used since no inference on which specific SNPs may be mispolarized, and since each block contains a relatively small number of SNPs, especially with respect to the mispolarization rate, cannot effectively use the overall mispolarization rate
def SAFEstats(hapsInSubWin,mappingDerivedInSubWin,dafsInSubWin):
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
      if hapsInSubWin[j][haplotypes[i][0]]==mappingDerivedInSubWin[j]:
        HAFunique[i]+=len([hapsInSubWin[j][x] for x in range(len(hapsInSubWin[j])) if hapsInSubWin[j][x]==mappingDerivedInSubWin[j]])
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
      if int(list(j)[i])==mappingDerivedInSubWin[i]:
        phi[i]+=(HAFunique[j]*len(haplotypes[j]))
        if HAFunique[j] not in kappa[i] and HAFunique[j]!=0:
          kappa[i].append(HAFunique[j])
      phiDenom+=(HAFunique[j]*len(haplotypes[j]))
    phi[i]/=float(phiDenom)
    kappa[i]=len(kappa[i])/float(len(set([HAFunique[x] for x in HAFunique if HAFunique[x]!=0])))
    if dafsInSubWin[i]==0 or dafsInSubWin[i]==1:
     SAFE.append(0.0)
    else:
     SAFE.append((phi[i]-kappa[i])/float(math.sqrt(dafsInSubWin[i]*(1-dafsInSubWin[i]))))
  statVals={}
  quantiles={"Lower95%":2.5,"Lower50%":25,"Upper50%":75,"Upper95%":97.5}
  for i in ["HAF", "HAFunique", "phi", "kappa", "SFS", "SAFE"]:
    if i=="SFS":
      windowStats=dafsInSubWin
    elif i=="HAFunique":
      windowStats=[eval(i)[x] for x in eval(i)]
    else:
      windowStats=eval(i)
    statVals[i+"-Mean"]=np.mean(windowStats)
    statVals[i+"-Median"]=np.median(windowStats)
    if(len(np.unique(windowStats,return_counts=True)[1])==1):
      statVals[i+"-Mode"]=windowStats[0]
    else:
      if(sorted(np.unique(windowStats,return_counts=True)[1])[-1]!=sorted(np.unique(windowStats,return_counts=True)[1])[-2]):
        statVals[i+"-Mode"]=scipy.stats.mstats.mode(windowStats)[0][0]
      else:
        mode=min(windowStats)
        for j in range(1,51):
          if len([x for x in windowStats if x >= (min(windowStats)+(j*((max(windowStats)-min(windowStats))/50))) and x < (min(windowStats)+((j+1)*((max(windowStats)-min(windowStats))/50)))]) >= len([x for x in windowStats if x >= mode and x < (mode+((max(windowStats)-min(windowStats))/50))]):
            mode=min(windowStats)+(j*((max(windowStats)-min(windowStats))/50))
        statVals[i+"-Mode"]=mode+((max(windowStats)-min(windowStats))/100)
    for j in quantiles:
      statVals[i+"-"+j]=np.percentile(windowStats,quantiles[j])
    statVals[i+"-Max"]=max(windowStats)
    statVals[i+"-Var"]=np.var(windowStats)
    statVals[i+"-SD"]=np.std(windowStats)
    statVals[i+"-Skew"]=scipy.stats.skew(windowStats)
    statVals[i+"-Kurt"]=scipy.stats.kurtosis(windowStats)
  return statVals

if segmentStart==None:
  firstSubWinStart=1
  lastSubWinStart=(((chrLen-1)/subWinSize)*subWinSize)+1
else:
  firstSubWinStart=(((segmentStart-1)/subWinSize)*subWinSize)+1
  lastSubWinStart=(((segmentEnd-1)/subWinSize)*subWinSize)+1
goodSubWins=[]
for i in range(numSubWins):
  goodSubWins.append(False)
subWinIndex=-1
def getSnpIndicesInSubWins(subWinSize,positions):
  subWinStart=1
  subWinEnd=subWinStart+subWinSize-1
  snpIndicesInSubWins=None
  for i in range(len(positions)):
    if snpIndicesInSubWins and not (positions[i]>=subWinStart and positions[i]<=subWinEnd):
      snpIndicesInSubWins.append([])
    while not (positions[i]>=subWinStart and positions[i]<=subWinEnd):
      subWinStart+=subWinSize
      subWinEnd+=subWinSize
    if not snpIndicesInSubWins:
      snpIndicesInSubWins=[[]]
    snpIndicesInSubWins[-1].append(i)
  return snpIndicesInSubWins
snpIndicesInSubWins=getSnpIndicesInSubWins(subWinSize,positions)
statVals={}
for statName in statNames:
  statVals[statName]=[]
if statFileName.lower() in ["none","false"]:
  statFileName=None
else:
  statFile=open(statFileName,"w")
  statFile.write(statHeader+"\n")
if fvecFileName.lower() in ["none","false","default"]:
  if segmentStart!=None:
    fvecFileName=targetPop+'.'+chrArm+'.'+segStart+'.fvec'
  else:
    fvecFileName=targetPop+'.'+chrArm+'.fvec'
fvecFile=open(fvecFileName,"w")
fvecFile.write(header+"\n")

for subWinStart in range(firstSubWinStart,lastSubWinStart+1,subWinSize):
  subWinEnd=subWinStart+subWinSize-1
  unmaskedFrac=unmasked[subWinStart-1:subWinEnd].count(True)/float(subWinSize)
  if len([x for x in positions if subWinStart<=x<=subWinEnd])==0:
    sys.stderr.write("window at positions %d-%d: number of unmasked SNPs - 0; fraction of sites unmasked - %f\n" %(subWinStart,subWinEnd,unmaskedFrac))
    goodSubWins.append(False)
  else:
    subWinIndex+=1
    sys.stderr.write("window at positions %d-%d: number of unmasked SNPs - %d; fraction of sites unmasked - %f\n" %(subWinStart,subWinEnd,len(snpIndicesInSubWins[subWinIndex]),unmaskedFrac))
    if unmaskedFrac<unmaskedFracCutoff:
      goodSubWins.append(False)
    else:
      goodSubWins.append(True)
      hapsInSubWin=haps.subset(sel0=snpIndicesInSubWins[subWinIndex])
      for statName in statNames:
        if statName!="H12" and statName!="H2/H1" and statName!="Omega" and statName!="distSkew" and statName!="distKurt" and statName[0:3]!="HAF" and statName[0:3]!="phi" and statName[0:3]!="kap" and statName[0:3]!="SFS" and statName[0:3]!="SAF":
          if statName=="fayWuH":
            calcAndAppendStatValForScan(alleleCounts, positions, statName, subWinStart, subWinEnd, statVals, (len(statVals["thetaH"])-1), hapsInSubWin, unmasked, precomputedStats)
          else:
            calcAndAppendStatValForScan(alleleCounts, positions, statName, subWinStart, subWinEnd, statVals, subWinIndex, hapsInSubWin, unmasked, precomputedStats)
      SAFEVals=SAFEstats(hapsInSubWin,[mapping[x][1] for x in snpIndicesInSubWins[subWinIndex]],dafs[snpIndicesInSubWins[subWinIndex]])
      for statName in SAFEVals:
        statVals[statName].append(SAFEVals[statName])
      if statFileName:
        statFile.write("\t".join([chrArm, str(subWinStart), str(subWinEnd)] + [str(statVals[statName][-1]) for statName in statNames]) + "\n")
  goodSubWins=goodSubWins[1:]
  if goodSubWins.count(True)==numSubWins:
    outVec=[]
    for statName in statNames:
      outVec+=normalizeFeatureVec(statVals[statName][-numSubWins:])
    midSubWinEnd=subWinEnd-(subWinSize*(numSubWins/2))
    midSubWinStart=midSubWinEnd-subWinSize+1
    fvecFile.write("\t".join([chrArm, str(midSubWinStart), str(midSubWinEnd), str((subWinEnd-(subWinSize*numSubWins)+1))+"-"+str(subWinEnd)] + [str(x) for x in outVec]) + "\n")

if statFileName:
  statFile.close()
fvecFile.close()
sys.stderr.write("total time spent calculating summary statistics and generating feature vectors: %g secs\n" %(time.clock()-startTime))
