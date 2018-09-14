#!/bin/bash

chrArms=("2L" "2R" "3L" "3R")
chrLens=(49364325 61545105 41963435 53200684)
stepSize=5000000
subWinSize=5000
numSubWins=11
mkdir -p data/
mkdir -p data/sumstats/
mkdir -p data/FVs/
mkdir -p data/logs/
for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir -p data/sumstats/$pop
  mkdir -p data/FVs/$pop
  mkdir -p data/logs/$pop
  for ((i=0; $i < ${#chrArms[@]} ; i++));
    do
    chrArm="${chrArms[$i]}"
    segmentStart=1
    segmentEnd=$(( $segmentStart - 1 + $stepSize + $subWinSize * ($numSubWins - 1) ))
    while [ $segmentStart -lt ${chrLens[$i]} ]
      do
      touch data/logs/$pop/$chrArm.$segmentStart.log;rm data/logs/$pop/$chrArm.$segmentStart.log
      echo "/home/axue/anaconda2/bin/python empirical_1/convert_to_FVs.py /san/data/ag1kg/haplotypes/ag1000g.phase1.ar3.haplotypes.$chrArm.h5 $chrArm ${chrLens[$i]} $segmentStart $segmentEnd $subWinSize $numSubWins 0.25 `python /san/personal/dan/ag1kg/demogInferenceStuff/stairwayPlotToPMisPol.py /san/personal/dan/ag1kg/demogInferenceStuff/spSummaryOutput/$pop.meru_mela.sfs.sp.summary` /san/personal/dan/ag1kg/shicScanPhaseI/partialStatsAndDafs/${pop}_partial_stats.txt /san/data/ag1kg/accessibility/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa /san/data/ag1kg/outgroups/anc.meru_mela.$chrArm.fa /san/data/ag1kg/samples_pops.txt $pop empirical_1/data/sumstats/$pop/$chrArm.$segmentStart.stats empirical_1/data/FVs/$pop/$chrArm.$segmentStart.fvec" | qsub -q HPblg7 -N SHIC -pe smp 3 -o empirical_1/data/logs/$pop/$chrArm.$segmentStart.log -e empirical_1/data/logs/$pop/$chrArm.$segmentStart.log
      segmentStart=$(( $segmentStart + $stepSize ))
      segmentEnd=$(( $segmentEnd + $stepSize ))
    done
  done
done
