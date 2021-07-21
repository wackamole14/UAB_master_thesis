import pandas as pd
import numpy as np
import os
import sys

column_names=['CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','format','TOM008','B59','I23','N25','T29A',\
'ZH26','A1','A2','A3','A4','A5','A6','A7','AB8','B1','B2','B3','B4','B6','ORE','AKA018','AKA017','COR014','COR018',\
'COR023','COR025','GIM012','GIM024','JUT008','JUT011','KIE094','LUN004','LUN007','MUN008','MUN009','MUN013','MUN015',\
'MUN016','MUN020','RAL059','RAL091','RAL176','RAL177','RAL375','RAL426','RAL737','RAL855','SLA001','STO022','TEN015','TOM007']

df = pd.read_csv(f'SV_results.VCF', sep='\t',skiprows=9, names=column_names)

df["Flavor"] = [x.replace("FL=","").strip() for z in df.INFO.str.split(";").tolist() for x in z if "FL=" in x]
df['ISO1']= ['ISO1' if x == 'CNV-R' else np.nan for x in df['Flavor']]
df["Num_Alleles"] = [x.replace("NA=","").strip() for z in df.INFO.str.split(";").tolist() for x in z if "NA=" in x]
df["CNV_ID"] = [x.replace("XI=","").strip() for z in df.INFO.str.split(";").tolist() for x in z if "XI=" in x]
df["Complex_Event"] = [x.replace("CE=","").strip() for z in df.INFO.str.split(";").tolist() for x in z if "CE=" in x]

#fix chromosome column
df['CHROM'] = [x.replace("chr","").strip() for x in df.CHROM]

sample_list=['TOM008', 'B59', 'I23', 'N25', 'T29A', 'ZH26', 'A1', 'A2', 'A3', 'A4',\
	'A5', 'A6', 'A7', 'AB8', 'B1', 'B2', 'B3', 'B4', 'B6', 'ORE', 'AKA018',\
	'AKA017', 'COR014', 'COR018', 'COR023', 'COR025', 'GIM012', 'GIM024',\
	'JUT008', 'JUT011', 'KIE094', 'LUN004', 'LUN007', 'MUN008', 'MUN009',\
	'MUN013', 'MUN015', 'MUN016', 'MUN020', 'RAL059', 'RAL091', 'RAL176',\
	'RAL177', 'RAL375', 'RAL426', 'RAL737', 'RAL855', 'SLA001', 'STO022',\
	'TEN015', 'TOM007']

for sample in sample_list:
	df.loc[((df['Flavor'] =='CNV-Q') & (df[sample] != 0)), sample] = sample
	df.loc[((df['Flavor'] =='CNV-Q') & (df[sample] == 0)), sample] = np.nan
	df.loc[((df['Flavor'] =='CNV-R') & (df[sample] != 0)), sample] = np.nan
	df.loc[((df['Flavor'] =='CNV-R') & (df[sample] == 0)), sample] = sample

sample_list.append('ISO1')

df['Genomes_present'] = df[sample_list].apply(lambda x: ';'.join(x.dropna().astype(str).values), axis=1)

df['LEN']= [len(x) for x in df['REF']]
df['END']= [df.at[x,'POS'] + df.at[x,'LEN'] for x in range(0, len(df['REF']))]
df_1= df[['CHROM','POS','END','CNV_ID','LEN','Flavor','Genomes_present','Num_Alleles','Complex_Event']]

#output the new file to manipulate
df_1.to_csv('reduced_SV_results.VCF' , index=False,  sep='\t', header=False)





