#!/bin/bash

mkdir -p sumstats_SAFE_stats/
mkdir -p FVs_SAFE_stats/
mkdir -p logs_SAFE_stats/
for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir -p sumstats_SAFE_stats/$pop
  mkdir -p FVs_SAFE_stats/$pop
  mkdir -p logs_SAFE_stats/$pop
  for j in `ls /nfs/kernlab_ISI/data/simulations/anoShic/phaseI/trainingData/$pop/sp*`
    do
    touch logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log;rm logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log
    echo "/home/axue/anaconda2/bin/python training_sims_2.0/convert_to_FVs.py ${j} 2L,2R,3L,3R 5000 11 0.25 `python /san/personal/dan/ag1kg/demogInferenceStuff/stairwayPlotToPMisPol.py /san/personal/dan/ag1kg/demogInferenceStuff/spSummaryOutput/$pop.meru_mela.sfs.sp.summary` /san/personal/dan/ag1kg/shicScanPhaseI/partialStatsAndDafs/${pop}_partial_stats.txt /san/data/ag1kg/accessibility/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa /san/data/ag1kg/outgroups/anc.meru_mela.fa training_sims_2.0/sumstats_SAFE_stats/$pop/ training_sims_2.0/FVs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.fvec" | qsub -q HPblg7 -N SHIC -pe smp 3 -o training_sims_2.0/logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log -e training_sims_2.0/logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log
  done
done
