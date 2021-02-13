import sys
import allel
import random
import numpy as np
from msTools import *
from fvTools import *
import time

'''usage example
python calcStatsAndDafForEachSnpSingleMsFile.py /san/data/dan/simulations/discoal_multipopStuff/spatialSVMSims/trainingSets/equilibNeut.msout.gz 110000 iHS nSL
'''

trainingDataFileName, totalPhysLen = sys.argv[1:3]
totalPhysLen = int(totalPhysLen)

hapArraysIn, positionArrays = msOutToHaplotypeArrayIn(trainingDataFileName, totalPhysLen)
numInstances = len(hapArraysIn)

header = "daf\tiHS\tnSL"
print header

dafs = []
start = time.clock()
numInstancesDone = 0

numSnpsDone = 0
for instanceIndex in range(numInstances):
    if instanceIndex % 10 == 0:
        sys.stderr.write("done wtih %d of %d instances (%d SNPs)\n" %(instanceIndex, numInstances, numSnpsDone))
    haps = allel.HaplotypeArray(hapArraysIn[instanceIndex], dtype='i1')
    genos = haps.to_genotypes(ploidy=2)
    ac = genos.count_alleles()
    sampleSizes = [sum(x) for x in ac]
    assert len(set(sampleSizes)) == 1
    dafs = ac[:,1]/float(sampleSizes[0])
    ihsVals = allel.stats.selection.ihs(haps, positionArrays[instanceIndex], use_threads=True, include_edges=False)
    nslVals = allel.stats.selection.nsl(haps, use_threads=True)
    assert len(dafs) == len(ihsVals) == len(nslVals)
    numSnpsDone += len(dafs)
    for i in range(len(dafs)):
        print "%g\t%g\t%g" %(dafs[i], ihsVals[i], nslVals[i])
    if numSnpsDone > 5000000:
        break
