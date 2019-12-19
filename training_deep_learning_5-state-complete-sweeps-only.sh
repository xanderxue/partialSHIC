#!/bin/bash

export KERAS_BACKEND=tensorflow
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python3 training_deep_learning_5-state-complete-sweeps-only.py trainingData/FVs_no_nSL/$pop/ default 11 89 0.1 trainingData/${pop}_5-state-complete-sweeps-only.hdf5 trainingData/${pop}_5-state-complete-sweeps-only.json trainingData/${pop}_5-state-complete-sweeps-only.npy >trainingData/${pop}_5-state-complete-sweeps-only.log 2>&1
done

