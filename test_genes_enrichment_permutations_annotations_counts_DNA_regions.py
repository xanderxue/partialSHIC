import sys,os,time,gzip

elementBedFileName, geneAnnotationGffFileName, termAnnotationBedFileName, permutationMasterDir, permutationFileName, tmpIntersectDir = sys.argv[1:]

def readGeneSetInElements(elementBedFileName):
    geneLs = []
    with open(elementBedFileName) as elementBedFile:
        for line in elementBedFile:
            line = line.strip("\n").split()
            if len(line) > 3:
                c, s, e, genes = line
                geneLs += genes.split(",")
    return geneLs

def readGenesAnnotationAndTerms(geneAnnotationGffFileName):
    genesToTerms = {}
    if geneAnnotationGffFileName.endswith(".gz"):
        openFunc = gzip.open
    else:
        openFunc = open
    with openFunc(geneAnnotationGffFileName) as geneAnnotationGffFile:
        for line in geneAnnotationGffFile:
            if not line.startswith("#"):
                c, source, annotType, s, e, blah1, strand, blah2, info = line.strip().split("\t")
                s, e = int(s), int(e)
                if not genesToTerms.has_key(annotType):
                    genesToTerms[annotType] = []
    return genesToTerms

def writeTermCountsForGeneSet(currSet, genesToTerms, outFileName):
    countH = {}
    for gene in currSet:
        if gene in genesToTerms:
            if not countH.has_key(gene):
                countH[gene] = 0
            countH[gene] += 1
    with open(outFileName, "w") as outFile:
        for term in countH:
            outFile.write("%s\t%d\n" %(term, countH[term]))

genesToTerms = readGenesAnnotationAndTerms(geneAnnotationGffFileName)

tmpIntersectFileName = "%s/real.%s.interCount" %(tmpIntersectDir, permutationFileName)
currSet = readGeneSetInElements(elementBedFileName)
writeTermCountsForGeneSet(currSet, genesToTerms, tmpIntersectFileName)

for permutationDir in os.listdir(permutationMasterDir):
    assert not "/" in permutationDir
    
    permutationFilePath = permutationMasterDir + "/" + permutationDir + "/" + permutationFileName
    if os.path.isfile(permutationFilePath):
        permutationSet = readGeneSetInElements(permutationFilePath)
        tmpIntersectFileName = "%s/%s.%s.interCount" %(tmpIntersectDir, permutationDir, permutationFileName)
        writeTermCountsForGeneSet(permutationSet, genesToTerms, tmpIntersectFileName)
