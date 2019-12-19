#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  for chrArm in 2L 2R 3L 3R
    do
    for x in `ls empiricalData/FVs/$pop/${chrArm}*|cut -d '.' -f 2|sort -n`
      do
      if [ $x == 1 ]
        then
        cp empiricalData/FVs/$pop/$chrArm.1.fvec empiricalData/FVs/$pop.$chrArm.fvec
      else
        cat empiricalData/FVs/$pop/$chrArm.$x.fvec|awk 'NR>1' >>empiricalData/FVs/$pop.$chrArm.fvec
      fi
    done
  done
done

