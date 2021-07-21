#!/bin/env python

import pandas as pd
import os   #os should be installled with python version in miniconda

def read_in_ref():
        for folder in os.listdir('/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/'):
                os.system(f'cd /homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}')
                for filename in os.listdir(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}'):
                        if filename.endswith('liftoff'):
                                with open(os.path.join(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}', filename)) as f:
                                        df = pd.read_csv(f, sep='\t', header=None)
                                        print(f"Started summary: {folder}")
                                        process_file(folder, df)

def process_file(filename, df):
# make columns, name columns, drop columns, and drop all but genes
        df.columns=['seqname','source','feature','start','end','Xscore','strand','Xframe','attributes']
# list comprehension, grab all the columns we need
        df.drop(df[df.feature != 'gene'].index, inplace=True)
        df["gene id"] = [x.replace("gene_id","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "gene_id" in x]
        df["name"] = [x.replace("gene_symbol","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "gene_symbol" in x]
        df["coverage"] = [x.replace("coverage","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "coverage" in x]
        df['seqID']= [float(x.replace("sequence_ID","").replace('"',"").strip()) for z in df.attributes.str.split(";").tolist() for x in z if "sequence_ID" in x]
        try:
                df['copy number']= [float(x.replace("extra_copy_number","").replace('"',"").strip()) for z in df.attributes.str.split(";").tolist() for x in z if "extra_copy_number" in x]
        except:
                df["copy number"] = [x.replace("extra_copy_number","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "extra_copy_number" in x]
        df['length'] = df['end']-df['start']
        df = df.drop(['start','source','attributes','feature','strand','end','Xscore','Xframe'], axis=1)
        df['seqname'] = df['seqname'].str.replace('Chr-','')
        df = df.drop(df[~df['seqname'].isin(['X', '3L','3R', '2L','2R'])].index)
# resolve FBgn0013687   
        exists ='FBgn0013687' in df['gene id'].values
        if exists == True:
                print('Resolved FBgn0013678')
                df.drop(df.loc[df['gene id']== 'FBgn0013687'].index, inplace=True)
                df.loc[-1] = [4,'FBgn0013687','mt:ori',0,0,0,3855]

        df['coverage'] = pd.to_numeric(df['coverage'], downcast="float")
        df['seqID'] = pd.to_numeric(df['seqID'], downcast="float")
        copy_number_vals= [0,' 0','0']
        df.loc[(df['copy number'].isin(copy_number_vals) ),'copy number'] = 0

        df.loc[(df['copy number'] != 0 ),'copy number'] = 1

        df.loc[(df['coverage'] > 0.79), 'coverage'] = 'Yes'
        df.loc[(df['coverage'] != 'Yes'), 'coverage'] = 'No'
        df.loc[(df['seqID'] > 0.79), 'seqID'] = 'Yes'
        df.loc[(df['seqID'] != 'Yes'), 'seqID'] = 'No'
        print(f"Finished summary: {filename}")

        df.to_csv(f'{filename}_sum.csv', index=False)
        os.system(f'cd ..')

#---------------------------
def make_ref_summary():
        df= pd.read_csv("/homes/users/hlindstadt/gonzalez_lab/CNV/dmel-all-r6.31.gtf", sep='\t', header=None)
        df.columns=['seqname','source','feature','start','end','Xscore','strand','Xframe','attributes']
        df.drop(df[df.feature != 'gene'].index, inplace=True)
        df = df.drop(df[~df['seqname'].isin(['X', '3L','3R', '2L','2R'])].index)
        df["gene id"] = [x.replace("gene_id","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "gene_id" in x]
        df["name"] = [x.replace("gene_symbol","").replace('"',"").strip() for z in df.attributes.str.split(";").tolist() for x in z if "gene_symbol" in x]
        df['reff length']=df['end']-df['start']
        df= df.drop(['start','name','seqname','source','attributes','feature','strand','end','Xscore','Xframe'], axis=1)
        df= df.sort_values(by=['reff length'])
        df['gene id'] = df['gene id'].str.replace('gene_id ','')
        df['gene id'] = df['gene id'].str.replace('"','')
        df['coverage'] = 0
        df['seqID'] = 0
        df['copy number'] = 0
        df['present'] = 1
        df['summary'] = 0
        print(f"Made ref_summary")
#output the reference summary, only contains gene ids and lengths of genes
        df.to_csv('ISO1_sum.csv', index=False)    
#---------------------------

def process_summaries(filename, df, df_ref):
        if filename != 'ISO1_sum.csv':
                global processed
# tidy the column names and add necessary columns       
                df= df.drop(['seqname','name','length'], axis=1)
                df= df.rename(columns={'length':'present'})
                df.insert(1, 'ref length', 0)
                df=df.drop_duplicates(subset='gene id')
                df['present'] = 1
	
# tidy column values  to numeric 
                df.loc[(df.coverage == 'Yes'),'coverage'] = 1
                df.loc[(df.coverage == 'No'),'coverage'] = 0
                df[['coverage']] = df[['coverage']].apply(pd.to_numeric)
                df.loc[(df.seqID == 'Yes'),'seqID'] = 1
                df.loc[(df.seqID == 'No'),'seqID'] = 0
                df[['seqID']] = df[['seqID']].apply(pd.to_numeric)
#also make sure all cells are numeric 
                df[['copy number']] = df[['copy number']].apply(pd.to_numeric)
                copy_number_vals= [0,' 0']
                df.loc[(df['copy number'].isin(copy_number_vals) ),'copy number'] = 1
                df.loc[(df['copy number'] != 0 ),'copy number'] = 1
                df['gene id'] = df['gene id'].str.replace(' ','')
# this will switch the compard file to be the latest one, to not overwrite the ref file.       
                if processed !=0:
                        df_ref= pd.read_csv('Liftoff_gene_summary.csv') 
# concat the dataframes 
                frames=[df_ref,df]
                concat = pd.concat(frames)
                ref_summary = concat.groupby(['gene id']).sum()
                ref_summary.sort_values(by=['ref length'])
# overwrite old combined file and switch to new file for next process run
                ref_summary.to_csv('Liftoff_gene_summary.csv')
        else:
                print('Started gene summary: ISO1')
#---------------------------
# 
def total_summary(filename,df):
        global processed
        data = {'Total genes': [0],'Total CNV': [0],'Total lacking coverage': [0],'Total lacking seqID': [0]}
        df_new = pd.DataFrame(data,columns=['Sample','Total genes','Total CNV','Total lacking seqID','Total lacking coverage'])
        
        filename,summary= filename.split('_')
        if filename == 'ISO1':
                df_new['Sample']= filename
                df_new['Total CNV'] = 0
                df_new['Total lacking seqID'] = 0
                df_new['Total lacking coverage'] = 0
                df_new['Total genes']= len(df)
                df_new['Total unique genes']= len(df['gene id'].unique())
                df_sum= pd.read_csv("Liftoff_total_summary.csv", sep=',')
                df= pd.concat([df_new, df_sum])
                df.to_csv('Liftoff_total_summary.csv', index=False)
        else:
                print(f"Added to total summary: {filename}")
                df_new['Sample']= filename

                cnvs = df['copy number'].value_counts()
                df_new['Total CNV'] = cnvs[1]

                seqid = df['seqID'].value_counts()
                df_new['Total lacking seqID'] = seqid[1]

                coverage = df['coverage'].value_counts()
                df_new['Total lacking coverage'] = coverage[1]

                df_new['Total genes']= len(df)
                df_new['Total unique genes']= len(df['gene id'].unique())
       
                if processed !=0:
                        df_sum= pd.read_csv("Liftoff_total_summary.csv", sep=',')
                        df= pd.concat([df_new, df_sum])
                        df.to_csv('Liftoff_total_summary.csv', index=False)
                else:
                        df_new.to_csv('Liftoff_total_summary.csv', index=False)

#---------------------------
def sort_Liftoff_total():

        sorter= ['B59','I23','N25','T29A','ZH26','A1','A2','A3','A4','A5','A6','A7','AB8','B1','B2',
        'B3','B4','B6','ORE','AKA017','AKA018','COR014','COR018','COR023','COR025','GIM012','GIM024',
        'JUT008','JUT011','KIE094','LUN004','LUN007','MUN008','MUN009','MUN013','MUN015','MUN016','MUN020',
        'RAL059','RAL091','RAL176','RAL177','RAL375','RAL426','RAL737','RAL855','SLA001','STO022','TEN015',
        'TOM007','TOM008','ISO1']
        
        df_sum = pd.read_csv('Liftoff_total_summary.csv')
        # Create a dummy df with the required list and the col name to sort on
        dummy = pd.Series(sorter, name = 'Sample').to_frame()
        sorted_df = pd.merge(dummy, df_sum, on = 'Sample', how = 'left')

        sorted_df['SRC'] = ['Long','Long','Long','Long','Long','Chakraborty','Chakraborty','Chakraborty',
        'Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty',
        'Chakraborty','Chakraborty','Chakraborty','Chakraborty','Rech','Rech','Rech','Rech',
        'Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech',
        'Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech',
        'Rech','Rech','Rech','Rech','ISO1']

        sorted_df.to_csv(f'Liftoff_total_summary.csv', index=False)
#---------------------------
processed = 0

def read_in_summaries():
        global processed
        df_ref = pd.read_csv('ref_summary.csv')
        for filename in os.listdir('/homes/users/hlindstadt/scratch/Liftoff_summaries'):
                if filename.endswith('_sum.csv'):
                        with open(os.path.join(f'/homes/users/hlindstadt/scratch/Liftoff_summaries', filename)) as f:
                                df = pd.read_csv(f)
                                print(f"Started gene summary:{filename}")
                                process_summaries(filename, df, df_ref)
                                total_summary(filename,df)
                                processed +=1
        print(f"Finished gene summaries")


def run():
        read_in_ref()
        total_genes, filter_euchromatin = make_ref_summary()
        euchromatin_genes= filter_euchromatin()

        read_in_summaries()
        sort_Liftoff_total()
run()
