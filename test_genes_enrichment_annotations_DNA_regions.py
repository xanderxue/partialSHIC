import sys, gzip
from overlapper import overlap

elementBedFileName, gencodeFileName, elementWinSize = sys.argv[1:]
elementWinSize = int(elementWinSize)

def getOverlappingWins(s, e, elementWinSize):
    wins = []
    firstWinStart = (s-1) - ((s-1) % elementWinSize) + 1
    lastWinStart = (e-1) - ((e-1) % elementWinSize) + 1
    for winStart in range(firstWinStart, lastWinStart+1, elementWinSize):
        winEnd = winStart + elementWinSize - 1
        wins.append((winStart, winEnd))
    return wins

def readGencodeFile(gencodeFileName, elementWinSize):
    annotH = {}
    if gencodeFileName.endswith(".gz"):
        openFunc = gzip.open
    else:
        openFunc = open
    with openFunc(gencodeFileName) as gencodeFile:
        for line in gencodeFile:
            if not line.startswith("#"):
                c, source, annotType, s, e, blah1, strand, blah2, info = line.strip().split("\t")
                s, e = int(s), int(e)
                overlappingWins = getOverlappingWins(s, e, elementWinSize)
                for winS, winE in overlappingWins:
                    key = (c, winS, winE)
                    if not annotH.has_key(key):
                        annotH[key] = []
                    annotH[key].append((c, s, e, annotType))
    return annotH

def initElementHFromFile(elementBedFileName, elementWinSize):
    elementH = {}
    with open(elementBedFileName) as elementBedFile:
        for line in elementBedFile:
            if not line.startswith("#") and not line.startswith("track"):
                c, s, e = line.strip().split()[:3]
                s, e = int(s)+1, int(e)
                assert e - s + 1 == elementWinSize
                elementH[(c, s, e)] = {}
    return elementH

def getGenesOverlappingEachElement(elementH, annotH):
    for c, s, e in annotH.keys():
        if elementH.has_key((c, s, e)):
            for annotC, annotS, annotE, geneName in annotH[(c, s, e)]:
                overRange = overlap(annotS, annotE, s, e)
                if overRange:
                    elementH[(c, s, e)][geneName] = 1
    return elementH

elementH = initElementHFromFile(elementBedFileName, elementWinSize)

annotH = readGencodeFile(gencodeFileName, elementWinSize)

getGenesOverlappingEachElement(elementH, annotH)

for c, s, e in elementH.keys():
    geneNames = sorted(elementH[(c, s, e)].keys())
    print "%s\t%s\t%s\t%s" %(c, s-1, e, ",".join(geneNames))
