#!/bin/bash

source activate python3
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python test_classifier_5-state_complete_only.py $pop/training_5-state_complete_only.npy ../FVs_SAFE_stats_no_nSL/$pop/ 11 89 $pop/ accuracy_5-state_complete_only confusion_matrix_5-state_complete_only.pdf
done
