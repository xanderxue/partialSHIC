#!/bin/bash

source activate python3
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  python test_classifier_binary_selection.py $pop/training_binary_selection.npy ../FVs_SAFE_stats_no_nSL/$pop/ 11 89 $pop/ accuracy_binary_selection thresholds.txt confusion_matrix_binary_selection.pdf roc_curve.pdf
done
