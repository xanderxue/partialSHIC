import sys

inFileName = sys.argv[1]

def getPMisFromStairwayPlotSummary(inFileName):
    with open(inFileName) as inFile:
        mode = 1
        for line in inFile:
            if line.startswith("pMisPol_median"):
                mode = 2
            elif line.startswith("mutation_per_site"):
                mode = 3
            elif mode == 2:
                pMisMed, pMisLow, pMisHigh = [float(x) for x in line.strip().split("\t")]
            elif mode == 3:
                pass
    return pMisMed

print getPMisFromStairwayPlotSummary(inFileName)
