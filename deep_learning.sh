#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p ../sims_training_2/FVs_SAFE_stats_no_nSL/$pop
  mkdir -p $pop
  echo "#!/bin/bash -l
#SBATCH -p gpu
#SBATCH -t 12:00:00
#SBATCH -J SHIC
#SBATCH --gres=gpu:2

cd /home/ax22/training_sims_2.3.1/$pop
source activate python3
export KERAS_BACKEND=tensorflow
for i in \`ls ../../sims_training_2/FVs_SAFE_stats/$pop/\`
do
cat ../../sims_training_2/FVs_SAFE_stats/$pop/\$i|cut -f 1-155,189- >../../sims_training_2/FVs_SAFE_stats_no_nSL/$pop/\$i
done
srun /home/ax22/anaconda2/envs/python3/bin/python ../deep_learning.py ../../sims_training_2/FVs_SAFE_stats_no_nSL/$pop/ default 11 89 0.1 training_weights.hdf5 training.json training.npy >deep_learning.log 2>&1
" >$pop/slurm.sh
  sbatch $pop/slurm.sh
done
