#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir -p trainingData/sumstats/$pop/
  mkdir -p trainingData/FVs/$pop/
  mkdir -p trainingData/logs/$pop/
  for j in `ls trainingData/$pop/sp*`
    do
    python2 training_convert_to_FVs.py $j 2L,2R,3L,3R 5000 11 0.25 `python2 mosquito_data_files/stairwayPlotToPMisPol.py mosquito_data_files/$pop.meru_mela.sfs.sp.summary` mosquito_data_files/${pop}_partial_stats.txt mosquito_data_files/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa mosquito_data_files/anc.meru_mela.fa trainingData/sumstats/$pop/ trainingData/FVs/$pop/`echo $j|cut -d '/' -f 3|cut -d '.' -f 1`.fvec >trainingData/logs/$pop/`echo $j|cut -d '/' -f 3|cut -d '.' -f 1`.log
  done
done

