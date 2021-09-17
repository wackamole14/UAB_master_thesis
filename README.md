# UAB_master_thesis




## Creating Liftoff files and summary

#### run_Liftoff.sh
- Take each assembly and run it though Liftoff. 
- output: ${FILE_NAME}\_liftoff


#### strain_summary.py
- Take the individual liftoff results files and turn them into short summary files. 
- output: '{filename}\_sum.csv'


#### Sum_Liftoff.py
- Input: take each of the liftoff results files and turn it into a summary
- Output: Liftoff_total_summary.csv



##  Creating SVMU results

#### SVMU_sub.sh 
- generate the SVMU results with the nucmer, liftoff and lastz inputs.
- Inputs:  {filename}.fa    (the raw assemblies), ${FILE}\_lastz.txt  (the lastz output), ${FILE}2ISO.mm.delta ( the nucmer output)
- Output: all files in the SVMU folder in /CNV/svmu



## Generating CNV data

#### prep_run_CNV2VCF.py

- In working directory have:
-- sorted_dmel-all-r6.31.gtf
-- varSplitter
-- checkOvl
-- comSplitter 
-- Han2VCF.py
-- CutTree.R
grab the {sample}.SV.info.txt files from the svmu results folder, get CNV-Q and CNV-R info only, export: sv.all.clean.txt


#### Han2VCF.py
- modified script, combines individual results into combined VCF format. 
- CNV2VCF_sub.sh



#### SV_Analysis.py
- Take the raw SVMU resultsand filter for euchromatin, and size. 


#### make_reduced_SV_results.VCF.py

- Takes input: SV_results.VCF  and gives output: reduced_SV_results.VCF. Summarizes the results in the VCF to one column show presence or absence of CNV in Genome (consolidates CNV_R, CNV_Q)

#### intersect_genes_TE.py
- Inputs: reduced_SV_results.VCF, also need sorted_dmel-all-r6.31.gtf. 
- Which of the unique CNV IDs contain protein coding, non-protein coding regions? TEs? Start woking with the reduced_SV_results.VCF file as it has all the CNVs, where they are present, coordinates, and unique IDs.
- Output: Num_tes_per_CNV.txt
- columns of Num_tes_per_CNV.txt: CNV_ID	Flavor	Genomes_present	G_ID	G_LEN	mRNA_count	Overlap	Num_samples	genic_region	Num_uniq_G_per_CNV	TE_LIST_PER_CNV	Samples_containing_TE	Num_TES_per_CNV

-------
### BOUNDARIES process:

#### boundaries.py

- This script grabs the liftoff results, and figures out the genes from a specified list, to figure out the euchromatin bouundaries. 
- boundaries_sub.sh


#### Find_nearest_gene_neighbor_boundary.ipynb

- This script is run on the files that did not have the genes we needed to find the euchromatin boundaries. This will find the nearest neighbor! 


#### make_bounds.py

- This takes all the corrected boundaries files, and grabs only the info we need to calculate the total euchromatin lengths. 

#### sum_boundaries.py

- This sums these euchromatin lengths. 

-------
#### SVMU_euchromatin.py

- Take in the Boundaries files and the SVMU results and filter for euchromatin regions on each chromosome. Turn these into sigle aggregate summary file that shows the SVMU results for each sample. Output: sorted_SVMU_summary.tsv


## TE analysis 

#### convert_TE_sheet.ipynb

- Converts TEAnnot files into a format that can be added to the master TE list created by Santiago. This adds shared and unique TEs, and updates the total count of samples that contain the TE, in order to later intersect that TE list with the CNV list. 
Input: New TEAnnot files (long files in this case)
Output:  All_TE_sheet.txt  


## Quality checks

#### Graphs_SVs_QC.ipynb

-  Check the concordance between the different sample sources


## Attempts that didn't make it to the paper:

#### compare_euchromatin_genes.ipynb
- This was to get all the euchromatin from all the samples, and calculate the number of bases involved... it works. 

