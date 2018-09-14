#!/bin/bash

source activate python3
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p ../FVs_SAFE_stats_no_nSL/$pop
  for i in `ls ../FVs_SAFE_stats/$pop/`
    do
    cat ../FVs_SAFE_stats/$pop/$i|cut -f 1-154,188- >../FVs_SAFE_stats_no_nSL/$pop/$i
  done
  python test_classifier.py $pop/training.npy ../FVs_SAFE_stats_no_nSL/$pop/ 11 89 $pop/ accuracy confusionmatrix.pdf
done
