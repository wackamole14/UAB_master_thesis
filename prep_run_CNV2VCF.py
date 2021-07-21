import pandas as pd 
import numpy as np
import os
import sys

#-------------------------------
#In working directory have:
#       sorted_dmel-all-r6.31.gtf
#       varSplitter
#       checkOvl
#       comSplitter 
#       CNV2VCF.py
#       CutTree.R
#-------------------------------
#0. grab the {sample}.SV.info.txt files from the svmu results folder, get CNV-Q and CNV-R info only, export: sv.all.clean.txt
def parse_sv_info_files():
	all_samples=pd.DataFrame(columns=['REF_CHROM','REF_START','REF_END','SV_TYPE','Q_CHROM','Q_START','Q_END','ID','LEN',\
	'COV_REF','COV_Q','Euchromatin','QTE_NAME','QTE_SIZE','QTE_OVERLAP','RTE_NAME','RTE_SIZE','RTE_OVERLAP','QGENE_ID','QGENE_NAME',\
	'QGENE_SIZE','QGENE_OVERLAP','RGENE_ID','RGENE_NAME','RGENE_SIZE','RGENE_OVERLAP','QTE_SIZE_OVERLAP','RTE_SIZE_OVERLAP'])

	for filename in os.listdir('/homes/users/hlindstadt/gonzalez_lab/CNV/svmu/'):
		if len(filename) < 7:
			with open(os.path.join(f'/homes/users/hlindstadt/gonzalez_lab/CNV/svmu/{filename}/Filtering', f'{filename}_SV_info.tsv')) as f:
				df = pd.read_csv(f, sep='\t')
				print(f"{filename}: started")
				single_sample =read_files(filename,df)
				all_samples = pd.concat([all_samples,single_sample])
				all_samples = all_samples.sort_values(['REF_CHROM','REF_START'])
	all_samples.to_csv(f'sv.all.clean.txt', index=False, sep='\t',header=False)
def read_files(filename, df):
# grab CNV-Q and CNV-R

	df = df.loc[((df['SV_TYPE'] == 'CNV-Q') | (df['SV_TYPE'] == 'CNV-R')),:]
	df_Q = df.copy()
	df_Q.drop(df_Q[df_Q.Euchromatin != True].index, inplace=True)
	df_Q['ID'] = [filename +"_" + str(x) for x in range(0,len(df_Q))]
	return df_Q

#output:  sv.all.clean.txt
#-------------------------------
#1.  Comsplitter: make the initial files with Chakraborty tools using sv.all.clean.txt (must have tools in wkdr: varSplitter , checkOvl, comSplitter )
def make_chakraborty():
	os.system('bedtools merge -d 10 -i sv.all.clean.txt -c 2,1,2,3,4,5,6,7,8,9,10,11 -o count,collapse,collapse,collapse,collapse,collapse,collapse,collapse,collapse,collapse,collapse,collapse -delim ";" > merge_table.txt')
# print
	os.system('./TOOLS/varSplitter merge_table.txt > split_table.txt')
	os.system('./TOOLS/checkOvl split_table.txt 0 id_file.txt > checkOvl.out')
	os.system('./TOOLS/comSplitter checkOvl.out > comSplitter.out')

#-------------------------------
def run_CNV2VCF():

#this also can be wrapped in an Sbatch job as this is a heavy process, (slurm job file alternate code requires file )

	#os.system('sbatch CNV2VCF_sub.sh')
	os.system('python ./TOOLS/CNV2VCF.py comSplitter.out id_file.txt locusseq ./TOOLS/CutTree.R > SV_results.VCF')

#output: SV_results.VCF
#-------------------------------


def run():
	#parse_sv_info_files()
	#make_chakraborty()
	#run_CNV2VCF()


#-------------------------------


run()
boundaries_MUN013_liftoff.csv
boundaries_MUN013_liftoff.csv


