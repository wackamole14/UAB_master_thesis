#!/bin/env python

import pandas as pd
import os   #os should be installled with python version in miniconda

def read_in_reff():
        for folder in os.listdir('/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/good_ones'):
                os.system(f'cd /homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/good_ones/{folder}')
                for filename in os.listdir(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/good_ones/{folder}'):
                        if filename.endswith('liftoff'):
                                with open(os.path.join(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/good_ones/{folder}', filename)) as f:
                                        df = pd.read_csv(f, sep='\t', header=None)
                                        print(f"{filename}: started")
                                        process_file(filename, df)


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
        df = df.drop(df[~df['seqname'].isin(['X', '3L','3R', '2L','2R','4'])].index)
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
        print(f"finished {filename}")

        df.to_csv(f'{filename}_sum.csv', index=False)
        os.system(f'cd ..')

def run():
        read_in_reff()

run()
