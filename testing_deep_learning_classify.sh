#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  #nSL stats were removed due to a bug found in the version of scikit-allel that was current at the time of our study
  mkdir -p testingData/FVs_no_nSL/$pop/
  for i in `ls testingData/FVs/$pop/`
    do
    cat testingData/FVs/$pop/$i|cut -f 1-154,188- >testingData/FVs_no_nSL/$pop/$i
  done
  python3 testing_deep_learning_classify.py trainingData/$pop.npy testingData/FVs_no_nSL/$pop/ 11 89 testingData/ ${pop}_accuracy ${pop}_confusion_matrix.pdf >testingData/$pop.log 2>&1
done

