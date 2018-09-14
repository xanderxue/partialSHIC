#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA KES UGS
  do
  python sample_FVs.py FVs_SAFE_stats/$pop/spNeut.fvec FVs_SAFE_stats/$pop/spHard_ FVs_SAFE_stats/$pop/spSoft_ FVs_SAFE_stats/$pop/spPartialHard_ FVs_SAFE_stats/$pop/spPartialSoft_ 5 0,1,2,3,4,6,7,8,9,10 FVs_SAFE_stats/$pop/ neut.fvec,hard.fvec,linkedHard.fvec,soft.fvec,linkedSoft.fvec,partialHard.fvec,linkedPartialHard.fvec,partialSoft.fvec,linkedPartialSoft.fvec
done
