#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  python2 training_sample_FVs.py trainingData/FVs/$pop/spNeut.fvec trainingData/FVs/$pop/spHard_ trainingData/FVs/$pop/spSoft_ trainingData/FVs/$pop/spPartialHard_ trainingData/FVs/$pop/spPartialSoft_ 5 0,1,2,3,4,6,7,8,9,10 trainingData/FVs/$pop/ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec
done

