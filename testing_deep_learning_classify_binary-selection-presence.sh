#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python3 testing_deep_learning_classify_binary-selection-presence.py trainingData/${pop}_binary-selection-presence.npy testingData/FVs_no_nSL/$pop/ 11 89 testingData/ ${pop}_accuracy_binary-selection-presence ${pop}_roc_thresholds.txt ${pop}_confusion_matrix_binary-selection-presence.pdf ${pop}_roc_curve.pdf >testingData/${pop}_binary-selection-presence.log 2>&1
done

