# partialSHIC

Steps involving both a Python and bash script with the same root filename are used in conjunction; the bash script contains an example command, specifically that which was invoked for our study, that allows simple operation of the Python script with customization via a few arguments

Training:
Convert training simulation files, in gzipped ms format (one per selective sweep class), into two-dimensional matrices (i.e. feature vector images) with convert_to_FVs_training.py and convert_to_FVs_training.sh
Sample from simulated feature vector images for equal representation of each selection state during training with sample_FVs.py and sample_FVs.sh
Heatmap visualization of simulated feature vector images for each selection state with visualize_FVs.sh 
Deep learning training from simulated feature vector images with deep_learning.py and deep_learning.sh
Deep learning training for five-state classification only (i.e. without partial sweeps, or completed sweeps only) from simulated feature vector images with deep_learning_5-state_complete_only.py and deep_learning_5-state_complete_only.sh
Deep learning training for binary classification only (i.e. between four sweep classes versus without direct selection) from simulated feature vector images with deep_learning_binary_selection.py and deep_learning_binary_selection.sh

Testing:
Convert testing simulation files, in gzipped ms format (one per selective sweep class), into two-dimensional matrices (i.e. feature vector images) with convert_to_FVs_testing.py and convert_to_FVs_testing.sh
Experimental test of optimized CNN classifier on simulated feature vector images with test_classifier.py and test_classifier.sh
Experimental test of optimized CNN five-state classifier on simulated feature vector images with test_classifier_5-state_complete_only.py and test_classifier_5-state_complete_only.sh
Experimental test of optimized CNN binary classifier on simulated feature vector images with test_classifier_binary_selection.py, test_classifier_binary_selection.sh, and roc.py

Empirical:
Convert empirical data files, in h5 format, into two-dimensional matrices (i.e. feature vector images) with convert_to_FVs_empirical.py, convert_to_FVs_empirical.sh, and merge_FVs.sh
Deep learning classification with optimized CNN of empirical feature vector images with deep_learning_classify.py and deep_learning_classify.sh
Convert sub-window summary statistics from feature vector images and classification calls into UCSC browser format for visualization via convert_format_UCSC_browser_visualization.sh
Permutation test on classification calls of significant enrichment in DNA regions with test_genes_enrichment_permutations_DNA_regions.py, test_genes_enrichment_annotations_DNA_regions.py, test_genes_enrichment_permutations_annotations_counts_DNA_regions.py, test_genes_enrichment_permutations_annotations_pvalues_DNA_regions.py, and test_genes_enrichment_permutations_annotations_DNA_regions.sh
Permutation test on classification calls of significant enrichment in IR genes and GO terms with test_genes_enrichment_permutations_annotations.sh (associated Python scripts in S/HIC + diploS/HIC repositories)
Permutation test on classification calls of significant enrichment for total sweep calls in IR genes and GO terms with test_genes_enrichment_permutations_annotations_selection_presence.sh (associated Python scripts in S/HIC + diploS/HIC repositories)
