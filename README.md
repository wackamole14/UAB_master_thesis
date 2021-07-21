# UAB_master_thesis



## Generating CNV data

#### prep_run_CNV2VCF.py

- In working directory have:
-       sorted_dmel-all-r6.31.gtf
-       varSplitter
-       checkOvl
-       comSplitter 
-       CNV2VCF.py
-       CutTree.R
grab the {sample}.SV.info.txt files from the svmu results folder, get CNV-Q and CNV-R info only, export: sv.all.clean.txt


#### make_reduced_SV_results.VCF.py

- Takes input: SV_results.VCF  and gives output: reduced_SV_results.VCF. Summarizes the results in the VCF to one column show presence or absence of CNV in Genome (consolidates CNV_R, CNV_Q)

#### intersect_genes_TE.py

- Which of the unique CNV IDs contain protein coding, non-protein coding regions? TEs? Start woking with the reduced_SV_results.VCF file as it has all the CNVs, where they are present, coordinates, and unique IDs.

#### SVMU_euchromatin.py

- Take in the Boundaries files and the SVMU results and filter for euchromatin regions on each chromosome. Turn these into sigle aggregate summary file that shows the SVMU results for each sample. Output: sorted_SVMU_summary.tsv


## TE analysis 

#### convert_TE_sheet.ipynb

- Converts TEAnnot files into a format that can be added to the master TE list created by Santiago. This adds shared and unique TEs, and updates the total count of samples that contain the TE, in order to later intersect that TE list with the CNV list. 


## Graphs 


## Quality checks

#### Graphs_SVs_QC.ipynb

-  Check the concordance between the different sample sources
