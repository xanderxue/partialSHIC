#!/bin/bash

export KERAS_BACKEND=tensorflow
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  #nSL stats were removed due to a bug found in the version of scikit-allel that was current at the time of our study
  mkdir -p trainingData/FVs_no_nSL/$pop/
  for i in `ls trainingData/FVs/$pop/`
    do
    cat trainingData/FVs/$pop/$i|cut -f 1-155,189- >trainingData/FVs_no_nSL/$pop/$i
  done
  python3 training_deep_learning.py trainingData/FVs_no_nSL/$pop/ default 11 89 0.1 trainingData/$pop.hdf5 trainingData/$pop.json trainingData/$pop.npy >trainingData/$pop.log 2>&1
done

