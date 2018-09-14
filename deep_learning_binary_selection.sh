#!/bin/bash

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p $pop
  echo "#!/bin/bash -l
#SBATCH -p gpu
#SBATCH -t 12:00:00
#SBATCH -J SHIC
#SBATCH --gres=gpu:2

cd /home/ax22/training_sims_2.3.1/$pop
source activate python3
export KERAS_BACKEND=tensorflow
srun /home/ax22/anaconda2/envs/python3/bin/python ../deep_learning_binary_selection.py ../../sims_training_2/FVs_SAFE_stats_no_nSL/$pop/ default 11 89 0.1 training_weights_binary_selection.hdf5 training_binary_selection.json training_binary_selection.npy >deep_learning_binary_selection.log 2>&1
" >$pop/slurm_binary_selection.sh
  sbatch $pop/slurm_binary_selection.sh
done
