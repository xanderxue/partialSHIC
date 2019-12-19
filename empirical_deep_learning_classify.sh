#!/bin/bash

#nSL stats were removed due to a bug found in the version of scikit-allel that was current at the time of our study
mkdir -p empiricalData/FVs_no_nSL/
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for chrArm in 2L 2R 3L 3R
    do
    cat empiricalData/FVs/$pop.$chrArm.fvec|cut -f 1-158,192- >empiricalData/FVs_no_nSL/$pop.$chrArm.fvec
    python3 empirical_deep_learning_classify.py trainingData/$pop.npy empiricalData/FVs_no_nSL/$pop.$chrArm.fvec 11 89 empiricalData/$pop.$chrArm.bed >empiricalData/$pop.$chrArm.log 2>&1
  done
done

