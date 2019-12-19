#!/bin/bash

export KERAS_BACKEND=tensorflow
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python3 training_deep_learning_binary-selection-presence.py trainingData/FVs_no_nSL/$pop/ default 11 89 0.1 trainingData/${pop}_binary-selection-presence.hdf5 trainingData/${pop}_binary-selection-presence.json trainingData/${pop}_binary-selection-presence.npy >trainingData/${pop}_binary-selection-presence.log 2>&1
done

