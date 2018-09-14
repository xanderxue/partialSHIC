#!/bin/bash

ex=!
scp -r axue@kerndev.rutgers.edu:~/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results ./
rm results/anoGam3.chrom.sizes results/bedToBigBed results/KES.bed
for i in L R; do for j in 2 3; do rm results/*${j}${i}.bed; done; done
for i in AOM BFM BFS CMS GAS GNS GWA KES UGS logs; do rm -r results/$i; done

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/permuteOrderOfSweepCallRunsByChr.py ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/permutations/$pop/
  cat results/$pop.bed|sed -e 's/chr//g' -e 's/Soft_/SoftComplete_/g' -e 's/Hard_/HardComplete_/g' -e 's/SoftPartial_/SoftIncomplete_/g' -e 's/HardPartial_/HardIncomplete_/g' >results/permutations/$pop.bed
  rm results/$pop.bed
  echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python permuteOrderOfSweepCallRunsByChr.py results/permutations/$pop.bed 10000 results/permutations/$pop/
" >$pop.slurm.sh
  sbatch $pop.slurm.sh
done
rm permuteOrderOfSweepCallRunsByChr.py *.slurm.sh slurm-*

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/getExonsOverlappingEachBedElementAllPerms.py ./
scp axue@kerndev.rutgers.edu:/home/dan/pytools/overlapper.py ./
scp axue@kerndev.rutgers.edu:/san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python getExonsOverlappingEachBedElementAllPerms.py results/permutations/$pop/ $class.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 results/permutations/$pop/
" >$pop.$class.slurm.sh
    sbatch $pop.$class.slurm.sh
  done
done
rm getExonsOverlappingEachBedElementAllPerms.py *.slurm.sh slurm-*

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/annotations/filtered/$pop/
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    grep -v track results/permutations/$pop.bed | grep $class | cut -f 1-3 >results/annotations/filtered/$pop/$class.bed
  done
  rm results/permutations/$pop.bed
done

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/getExonsOverlappingEachBedElement.py ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/annotations/$pop/
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python getExonsOverlappingEachBedElement.py results/annotations/filtered/$pop/$class.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 >results/annotations/$pop/$class.bed
" >$pop.$class.slurm.sh
    sbatch $pop.$class.slurm.sh
  done
done
rm getExonsOverlappingEachBedElement.py overlapper.py overlapper.pyc *.slurm.sh slurm-*

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/doPermutationCountsOfAllGeneSets.py ./
scp -r axue@kerndev.rutgers.edu:/san/data/ag1kg/geneListsFromNick/ ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for geneSetFile in `ls geneListsFromNick/`
    do
    mkdir -p results/permutations/counts_IR/$pop/$geneSetFile/
  done
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python doPermutationCountsOfAllGeneSets.py results/annotations/$pop/$class.bed geneListsFromNick/ results/permutations/$pop/ $class.bed results/permutations/counts_IR/$pop/ 10000
" >$pop.$class.slurm.sh
    sbatch $pop.$class.slurm.sh
  done
done
rm doPermutationCountsOfAllGeneSets.py *.slurm.sh slurm-*
rm -r geneListsFromNick/

scp axue@kerndev.rutgers.edu:/san/personal/dan/ag1kg/shicScanPhaseI/doPermutationCountsOfTermAnnotElements.py ./
scp axue@kerndev.rutgers.edu:/san/data/GO/GO-Basic_Downloaded_2_18_2015/go.* ./
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for namespace in biological_process molecular_function cellular_component
    do
    mkdir -p results/permutations/counts_GO/$pop/$namespace/
    for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
      do
      echo "#${ex}/bin/bash -l
#SBATCH -p main
#SBATCH -t 12:00:00
#SBATCH -J SHIC

cd /home/ax22/
srun /home/ax22/anaconda2/bin/python doPermutationCountsOfTermAnnotElements.py results/annotations/$pop/$class.bed Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz go.$namespace.txt results/permutations/$pop/ $class.bed results/permutations/counts_GO/$pop/$namespace/
" >$pop.$namespace.$class.slurm.sh
      sbatch $pop.$namespace.$class.slurm.sh
    done
  done
done
rm doPermutationCountsOfTermAnnotElements.py Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz go.* *.slurm.sh slurm-*
scp -r results/annotations axue@kerndev.rutgers.edu:~/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/
scp -r results/permutations axue@kerndev.rutgers.edu:~/Detecting_partial_sweeps_Anopheles_mosquito/empirical_4/results/
rm -r results



mkdir -p results/permutations_annotations_test/
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "Enrichment results for $pop" >results/permutations_annotations_test/$pop.txt
  for bedFile in `ls /san/data/ag1kg/geneListsFromNick/`
    do
    for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
      do
      python /san/personal/dan/ag1kg/shicScanPhaseI/getPermutationPValsOfGeneSets.py results/permutations/counts_IR/$pop/$bedFile/ $class.bed.interCount >>results/permutations_annotations_test/$pop.txt
    done
  done
done

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/permutations_annotations_test/$pop/
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    for namespace in biological_process molecular_function cellular_component
      do
      python /san/personal/dan/ag1kg/shicScanPhaseI/getPermutationQValsOfTermAnnotElements.py results/permutations/counts_GO/$pop/$namespace/ $class.bed.interCount /san/data/GO/GO-Basic_Downloaded_2_18_2015/go.$namespace.txt >results/permutations_annotations_test/$pop/${class}_$namespace.txt
    done
  done
done
