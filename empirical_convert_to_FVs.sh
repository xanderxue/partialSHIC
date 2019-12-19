#!/bin/bash

chrArms=("2L" "2R" "3L" "3R")
chrLens=(49364325 61545105 41963435 53200684)
stepSize=5000000
subWinSize=5000
numSubWins=11
for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  mkdir -p empiricalData/sumstats/$pop/
  mkdir -p empiricalData/FVs/$pop/
  mkdir -p empiricalData/logs/$pop/
  for ((i=0; $i < ${#chrArms[@]} ; i++));
    do
    chrArm="${chrArms[$i]}"
    segmentStart=1
    segmentEnd=$(( $segmentStart - 1 + $stepSize + $subWinSize * ($numSubWins - 1) ))
    while [ $segmentStart -lt ${chrLens[$i]} ]
      do
      python2 empirical_convert_to_FVs.py empiricalData/ag1000g.phase1.ar3.haplotypes.$chrArm.h5 $chrArm ${chrLens[$i]} $segmentStart $segmentEnd $subWinSize $numSubWins 0.25 `python2 mosquito_data_files/stairwayPlotToPMisPol.py mosquito_data_files/$pop.meru_mela.sfs.sp.summary` mosquito_data_files/${pop}_partial_stats.txt mosquito_data_files/Anopheles-gambiae-PEST_CHROMOSOMES_AgamP3.accessible.fa mosquito_data_files/anc.meru_mela.$chrArm.fa mosquito_data_files/samples_pops.txt $pop empiricalData/sumstats/$pop/$chrArm.$segmentStart.stats empiricalData/FVs/$pop/$chrArm.$segmentStart.fvec > empiricalData/logs/$pop/$chrArm.$segmentStart.log
      segmentStart=$(( $segmentStart + $stepSize ))
      segmentEnd=$(( $segmentEnd + $stepSize ))
    done
  done
done

