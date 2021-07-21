import pandas as pd
import numpy as np
import os
import sys

dir_svmu= "/Users/hannahlindstadt/Gonzalez_lab_local/svmu/svmu/"
dir_boundaries= "/Users/hannahlindstadt/Gonzalez_lab_local/liftoff/drive_boundaries/"

def read_in_files():
    df_all=0
    first_run=True
    for folder in os.listdir(f'{dir_svmu}'):
        for filename in os.listdir(f'{dir_svmu}/{folder}'):
            if filename.startswith('sv.') & filename.endswith('.txt'):
                #SV,filename,txt= filename.str.split('.')
                with open(os.path.join(f'{dir_boundaries}', f'boundaries_{folder}_liftoff.csv')) as f:
                    df_boundaries = pd.read_csv(f, sep=',')
                with open(os.path.join(f'{dir_svmu}/{folder}', f'{filename}')) as f1:
                    df_svmu = pd.read_csv(f1, sep='\t')
                    print(f"{filename}: started")
                    entry = process_file(folder, df_boundaries,df_svmu)
                    print(entry)
                    if first_run==True:
                        df_entry_columns= ['DEL','INS','nCNV-Q','nCNV-R','CNV-Q','CNV-R','INV','Total_SVs','Sample']
                        df_all = pd.DataFrame([entry], columns = df_entry_columns)
                        first_run = False
                    else:                   
                        df_length = len(df_all)
                        df_all.loc[df_length] = entry
    df_all.to_csv('SVMU_summary.tsv', sep='\t', index=False)


def process_file(folder, df_boundaries, df1):

    chromosomes = ['2L','2R','3L','3R','X']
    for chromosome in chromosomes:
        df_boundaries = df_boundaries.groupby(['seqname']).agg({'start':'min','end':'max'}).reset_index()
        df_boundaries.to_csv(f'{folder}_new_boundary.tsv', sep='\t', index=False)

    start = df_boundaries['start']
    end = df_boundaries['end']
    drop_indexes=[]

    for row in df1.index:
        if df1.at[row,'REF_CHROM'] == '2L':
            if df1.at[row,'REF_START'] < start[0]:
                drop_indexes.append(row)
            if df1.at[row,'REF_END'] > end[0]:
                drop_indexes.append(row)
        if df1.at[row,'REF_CHROM'] == '2R':
            if df1.at[row,'REF_START'] < start[1]:
                drop_indexes.append(row)
            if df1.at[row,'REF_END'] > end[1]:
                drop_indexes.append(row)          
        if df1.at[row,'REF_CHROM'] == '3L':
            if df1.at[row,'REF_START'] < start[2]:
                drop_indexes.append(row)
            if df1.at[row,'REF_END'] > end[2]:
                drop_indexes.append(row)            
        if df1.at[row,'REF_CHROM'] == '3R':
            if df1.at[row,'REF_START'] < start[3]:
                drop_indexes.append(row)
            if df1.at[row,'REF_END'] > end[3]:
                drop_indexes.append(row)        
        if df1.at[row,'REF_CHROM'] == 'X':
            if df1.at[row,'REF_START'] < start[4]:
                drop_indexes.append(row)
            if df1.at[row,'REF_END'] > end[4]:
                drop_indexes.append(row)

    df_euchromatin = df1.drop(drop_indexes)
    total_euchromatin_SV= len(df_euchromatin)
    entry = df_euchromatin['SV_TYPE'].value_counts().tolist()
    entry.append(total_euchromatin_SV)
    entry.append(folder)

    return entry

def sort_SVMU_totals():

    sorter= ['B59','I23','N25','T29A','ZH26','A1','A2','A3','A4','A5','A6','A7','AB8','B1','B2',
    'B3','B4','B6','ORE','AKA017','AKA018','COR014','COR018','COR023','COR025','GIM012','GIM024',
    'JUT008','JUT011','KIE094','LUN004','LUN007','MUN008','MUN009','MUN013','MUN015','MUN016','MUN020',
    'RAL059','RAL091','RAL176','RAL177','RAL375','RAL426','RAL737','RAL855','SLA001','STO022','TEN015',
    'TOM007','TOM008']
    
    df_sum = pd.read_csv('SVMU_summary.tsv', sep='\t')
    #df_sum = pd.read_csv('tmp', sep='\t')
    
    # Create a dummy df with the required list and the col name to sort on
    dummy = pd.Series(sorter, name = 'Sample').to_frame()
    sorted_df = pd.merge(dummy, df_sum, on = 'Sample', how = 'left')

    sorted_df['SRC'] = ['Long','Long','Long','Long','Long','Chakraborty','Chakraborty','Chakraborty',
    'Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty','Chakraborty',
    'Chakraborty','Chakraborty','Chakraborty','Chakraborty','Rech','Rech','Rech','Rech',
    'Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech',
    'Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech','Rech',
    'Rech','Rech','Rech','Rech']

    sorted_df.to_csv(f'sorted_SVMU_summary.tsv', index=False)


def run():
    read_in_files()
    sort_SVMU_totals()


run()

