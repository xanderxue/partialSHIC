#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python3 testing_deep_learning_classify_5-state-complete-sweeps-only.py trainingData/${pop}_5-state-complete-sweeps-only.npy testingData/FVs_no_nSL/$pop/ 11 89 testingData/ ${pop}_accuracy_5-state-complete-sweeps-only ${pop}_confusion_matrix_5-state-complete-sweeps-only.pdf >testingData/${pop}_5-state-complete-sweeps-only.log 2>&1
done

