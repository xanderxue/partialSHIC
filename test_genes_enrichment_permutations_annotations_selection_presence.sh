#!/bin/bash

ex=!
mkdir -p results/permutations_selection_presence
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  scp axue@kerndev.rutgers.edu:~/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/$pop.bed ./
done

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/permuteOrderOfSweepCallRunsByChr.py ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  cat $pop.bed|sed -e 's/chr//g' -e "s/Soft_/${pop}_/g" -e "s/Hard_/${pop}_/g" -e "s/SoftPartial_/${pop}_/g" -e "s/HardPartial_/${pop}_/g" >results/permutations_selection_presence/$pop.bed
  rm $pop.bed
  echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python permuteOrderOfSweepCallRunsByChr.py results/permutations_selection_presence/$pop.bed 10000 results/permutations_selection_presence/
" >$pop.slurm.sh
  sbatch $pop.slurm.sh
done
rm permuteOrderOfSweepCallRunsByChr.py *.slurm.sh slurm-*

mkdir -p results/annotations_selection_presence/filtered/
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  grep -v track results/permutations_selection_presence/$pop.bed | grep "$pop" | cut -f 1-3 >results/annotations_selection_presence/filtered/$pop.bed
  rm results/permutations_selection_presence/$pop.bed
done

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/getExonsOverlappingEachBedElementAllPerms.py ./
scp axue@kerndev.rutgers.edu:/home/dan/pytools/overlapper.py ./
scp axue@kerndev.rutgers.edu:/san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python getExonsOverlappingEachBedElementAllPerms.py results/permutations_selection_presence/ $pop.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 results/permutations_selection_presence/
" >$pop.slurm.sh
  sbatch $pop.slurm.sh
done
for i in {0..9999}
  do
  rm results/permutations_selection_presence/permutation_$i/Neutral.bed
  rm results/permutations_selection_presence/permutation_$i/*-linked.bed
done
rm getExonsOverlappingEachBedElementAllPerms.py *.slurm.sh slurm-*

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/getExonsOverlappingEachBedElement.py ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python getExonsOverlappingEachBedElement.py results/annotations_selection_presence/filtered/$pop.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 >results/annotations_selection_presence/$pop.bed
" >$pop.slurm.sh
  sbatch $pop.slurm.sh
done
rm getExonsOverlappingEachBedElement.py overlapper.py overlapper.pyc *.slurm.sh slurm-*

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/doPermutationCountsOfAllGeneSets.py ./
scp -r axue@kerndev.rutgers.edu:/san/data/ag1kg/geneListsFromNick/ ./
for geneSetFile in `ls geneListsFromNick/`
  do
  mkdir -p /scratch/ax22/results/permutations_selection_presence/counts_IR/$geneSetFile/
done
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python doPermutationCountsOfAllGeneSets.py results/annotations_selection_presence/$pop.bed geneListsFromNick/ results/permutations_selection_presence/ $pop.bed /scratch/ax22/results/permutations_selection_presence/counts_IR/ 10000
" >$pop.slurm.sh
  sbatch $pop.slurm.sh
done
rm doPermutationCountsOfAllGeneSets.py *.slurm.sh slurm-*
rm -r geneListsFromNick/

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/doPermutationCountsOfTermAnnotElements.py ./
scp axue@kerndev.rutgers.edu:/san/data/GO/GO-Basic_Downloaded_2_18_2015/go.* ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for namespace in biological_process molecular_function cellular_component
    do
    mkdir -p /scratch/ax22/results/permutations_selection_presence/counts_GO/$namespace/
    echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python doPermutationCountsOfTermAnnotElements.py results/annotations_selection_presence/$pop.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz go.$namespace.txt results/permutations_selection_presence/ $pop.bed /scratch/ax22/results/permutations_selection_presence/counts_GO/$namespace/
" >$pop.$namespace.slurm.sh
    sbatch $pop.$namespace.slurm.sh
  done
done
rm doPermutationCountsOfTermAnnotElements.py Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz go.* *.slurm.sh slurm-*
scp -r results/annotations_selection_presence axue@kerndev.rutgers.edu:/nfs/kernlab_ISI/Xander_kerndev/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/
scp -r results/permutations_selection_presence axue@kerndev.rutgers.edu:/nfs/kernlab_ISI/Xander_kerndev/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/
scp -r /scratch/ax22/results/permutations_selection_presence/counts_IR axue@kerndev.rutgers.edu:/nfs/kernlab_ISI/Xander_kerndev/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/permutations_selection_presence/
scp -r /scratch/ax22/results/permutations_selection_presence/counts_GO axue@kerndev.rutgers.edu:/nfs/kernlab_ISI/Xander_kerndev/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/permutations_selection_presence/
rm -r results /scratch/ax22/results



mkdir -p results/permutations_annotations_test_selection_presence/
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "Enrichment results for $pop" >results/permutations_annotations_test_selection_presence/${pop}_IR.txt
  for bedFile in `ls /san/data/ag1kg/geneListsFromNick/`
    do
    python /san/personal/dan/ag1kg/shicScanPhaseI/getPermutationPValsOfGeneSets.py results/permutations_selection_presence/counts_IR/$bedFile/ $pop.bed.interCount >>results/permutations_annotations_test_selection_presence/${pop}_IR.txt
  done
done

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for namespace in biological_process molecular_function cellular_component
    do
    python /san/personal/dan/ag1kg/shicScanPhaseI/getPermutationQValsOfTermAnnotElements.py results/permutations_selection_presence/counts_GO/$namespace/ $pop.bed.interCount /san/data/GO/GO-Basic_Downloaded_2_18_2015/go.$namespace.txt >results/permutations_annotations_test_selection_presence/${pop}_$namespace.txt
  done
done
