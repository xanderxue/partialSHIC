source activate python3
mkdir -p empirical_4.5/results
mkdir -p empirical_4.5/results/logs
mkdir -p empirical_4.5/data/FVs

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for chrArm in 2L 2R 3L 3R
    do
    cat ../data/FVs/$pop.$chrArm.fvec|cut -f 1-158,192- >data/FVs/$pop.$chrArm.fvec
    echo "/home/axue/anaconda2/envs/python3/bin/python empirical_4.5/deep_learning_classify.py empirical_4.5/$pop/training.npy empirical_4.5/data/FVs/$pop.$chrArm.fvec 11 89 empirical_4.5/results/$pop.$chrArm.bed" | qsub -q HPblg7 -w e -N anoShic -pe smp 2 -o empirical_4.5/results/logs/$pop.$chrArm.log -e empirical_4.5/results/logs/$pop.$chrArm.log
  done
done
