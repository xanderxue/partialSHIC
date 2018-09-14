#!/bin/bash

cp /home/dan/pytools/overlapper.py ./
mv results/permutations_selection_presence/counts* results/permutations_selection_presence/permutation_0/
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/permutations_DNA_regions/$pop
  for i in {0..9999}
    do
    mkdir -p results/permutations_DNA_regions/$pop/permutation_$i
  done
  mkdir -p results/annotations_DNA_regions/$pop
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    mkdir -p $pop.$class
    cd $pop.$class
    echo "/home/axue/anaconda2/bin/python ../test_genes_enrichment_permutations_DNA_regions.py ../results/permutations/$pop/ $class.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 ../results/permutations_DNA_regions/$pop
    " >Script.sh
    screen -S $pop.$class
    cd ..
    /home/axue/anaconda2/bin/python test_genes_enrichment_annotations_DNA_regions.py results/annotations/filtered/$pop/$class.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 >results/annotations_DNA_regions/$pop/$class.bed
  done
  mkdir -p $pop
  cd $pop
  echo "/home/axue/anaconda2/bin/python ../test_genes_enrichment_permutations_DNA_regions.py ../results/permutations_selection_presence/ $pop.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 ../results/permutations_DNA_regions/$pop
  " >Script.sh
  screen -S $pop.selection
  cd ..
  /home/axue/anaconda2/bin/python test_genes_enrichment_annotations_DNA_regions.py results/annotations_selection_presence/filtered/$pop.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz 5000 >results/annotations_DNA_regions/$pop/$pop.bed
done
mv results/permutations_selection_presence/permutation_0/counts* results/permutations_selection_presence/
rm test_genes_enrichment_permutations_DNA_regions.py test_genes_enrichment_annotations_DNA_regions.py overlapper.py overlapper.pyc

for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  mkdir -p results/permutations_DNA_regions/counts/$pop/
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    cd $pop.$class
    echo "/home/axue/anaconda2/bin/python ../test_genes_enrichment_permutations_annotations_counts_DNA_regions.py ../results/annotations_DNA_regions/$pop/$class.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz NULL ../results/permutations_DNA_regions/$pop/ $class.bed ../results/permutations_DNA_regions/counts/$pop/
    " >Script.sh
    screen -S $pop.$class
    cd ..
  done
  cd $pop
  echo "/home/axue/anaconda2/bin/python ../test_genes_enrichment_permutations_annotations_counts_DNA_regions.py ../results/annotations_DNA_regions/$pop/$pop.bed /san/data/ag1kg/geneset/Anopheles-gambiae-PEST_BASEFEATURES_AgamP4.7.gff3.gz NULL ../results/permutations_DNA_regions/$pop/ $pop.bed ../results/permutations_DNA_regions/counts/$pop/
  " >Script.sh
  screen -S $pop.selection
  cd ..
done
rm test_genes_enrichment_permutations_annotations_counts_DNA_regions.py
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  for class in Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    rm $pop.$class/Script.sh
    rmdir $pop.$class
  done
  rm $pop/Script.sh
  rmdir $pop
done

mkdir -p results/permutations_annotations_test_DNA_regions
for pop in AOM BFM BFS CMS GAS GNS GWA UGS
  do
  echo "Enrichment results for $pop" >results/permutations_annotations_test_DNA_regions/$pop.txt
  for class in $pop Neutral HardComplete Hard-linked SoftComplete Soft-linked HardIncomplete HardPartial-linked SoftIncomplete SoftPartial-linked
    do
    echo "$class" >>results/permutations_annotations_test_DNA_regions/$pop.txt
    python test_genes_enrichment_permutations_annotations_pvalues_DNA_regions.py results/permutations_DNA_regions/counts/$pop $class.bed.interCount >>results/permutations_annotations_test_DNA_regions/$pop.txt
  done
done
rm test_genes_enrichment_permutations_annotations_pvalues_DNA_regions.py
