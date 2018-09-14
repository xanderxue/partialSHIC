import sys,os

intersectCountDir, intersectFileSuffix = sys.argv[1:]

def readIntersectCounts(intersectFileName, countH):
    with open(intersectFileName) as intersectFile:
        for line in intersectFile:
            term, count = line.strip().split()
            count = int(count)
            if not countH.has_key(term):
                countH[term] = 0
            countH[term] += count

realCountH = {}
readIntersectCounts(intersectCountDir + "/real." + intersectFileSuffix, realCountH)
permCounts = []
for intersectFileName in os.listdir(intersectCountDir):
    if intersectFileName.endswith(intersectFileSuffix) and "real" not in intersectFileName:
        permCountH = {}
        for term in realCountH:
            permCountH[term] = 0
        readIntersectCounts(intersectCountDir + "/" + intersectFileName, permCountH)
        permCounts.append(permCountH)

totalCountH = {}
outLineH = {}
for term in realCountH:
    pCount = 0
    totalCount = 0
    permutedIntersectSum = 0
    for permCountH in permCounts:
        if permCountH.has_key(term):
            permCount = permCountH[term]
        else:
            permCount = 0
        permutedIntersectSum += permCount
        if permCount >= realCountH[term]:
            pCount += 1
        totalCount += 1
    totalCountH[totalCount] = 1
    meanIntersect = permutedIntersectSum/float(totalCount)
    if meanIntersect > 0:
        enrichment = realCountH[term] / meanIntersect
    else:
        enrichment = float("inf")
    if pCount == 0:
        pValStr = "<%s" %(1.0/totalCount)
    else:
        pValStr = str(pCount / float(totalCount))
    if not outLineH.has_key(pCount):
        outLineH[pCount] = []
    outLineH[pCount].append((enrichment, "%s; real intersect: %s; mean permuted intersect: %s; enrichment: %s; p-value: %s" %(term, realCountH[term], meanIntersect, enrichment, pValStr)))
assert len(totalCountH) == 1
totalCount = totalCountH.keys()[0]

positiveCount = len(realCountH)
minQVal=1.0
minNonZeroQVal=1.0
for pCount in sorted(outLineH, reverse=True):
    pVal = pCount/float(totalCount)
    fdr = (pVal*len(realCountH))/positiveCount
    if fdr < minQVal:
        if fdr != 0:
            minNonZeroQVal = fdr
        minQVal = fdr
    if minQVal > 0:
        qValStr = str(minQVal)
    else:
        qVal = ((1/float(totalCount))*len(realCountH))/positiveCount
        if qVal < minNonZeroQVal:
            qValStr = "<%s" %(qVal)
        else:
            qValStr = "<%s" %(minNonZeroQVal)
    outLines = []
    for enrichment, outLine in sorted(outLineH[pCount]):
        print outLine + "; q-value: %s" %(qValStr)
    positiveCount -= len(outLineH[pCount])	
