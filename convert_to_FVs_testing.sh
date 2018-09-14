#!/bin/bash

ex=!
mkdir -p /scratch/ax22/testing_sims_2.0
mkdir -p /scratch/ax22/testing_sims_2.0/sumstats_SAFE_stats/
mkdir -p /scratch/ax22/testing_sims_2.0/FVs_SAFE_stats/
mkdir -p /scratch/ax22/testing_sims_2.0/logs_SAFE_stats/
for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir -p /scratch/ax22/testing_sims_2.0/sumstats_SAFE_stats/$pop
  mkdir -p /scratch/ax22/testing_sims_2.0/FVs_SAFE_stats/$pop
  mkdir -p /scratch/ax22/testing_sims_2.0/logs_SAFE_stats/$pop
  for j in `ls ../testData/$pop/sp*`
    do
    touch /scratch/ax22/testing_sims_2.0/logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log;rm /scratch/ax22/testing_sims_2.0/logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log
    echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 24:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python testing_sims_2.0/convert_to_FVs.py `echo ${j}|cut -d '/' -f 2-` 2L,2R,3L,3R 5000 11 0.25 `python ../stairwayPlotToPMisPol.py ../spSummaryOutput/$pop.meru_mela.sfs.sp.summary` partialStatsAndDafs/${pop}_partial_stats.txt Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa outgroups/anc.meru_mela.fa /scratch/ax22/testing_sims_2.0/sumstats_SAFE_stats/$pop/ /scratch/ax22/testing_sims_2.0/FVs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.fvec >/scratch/ax22/testing_sims_2.0/logs_SAFE_stats/$pop/`echo ${j}|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.log 2>&1
" >$pop.`echo $j|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.slurm.sh
  sbatch $pop.`echo $j|rev|cut -d '/' -f 1|rev|cut -d '.' -f 1`.slurm.sh
  done
done
