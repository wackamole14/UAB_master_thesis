!/bin/env python

import pandas as pd
import os   #os should be installled with python version in miniconda

def read_in_reff():
        for folder in os.listdir('/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff'):
                os.system(f'cd /homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}')
                for filename in os.listdir(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}'):
                        if filename.endswith('liftoff'):
                                with open(os.path.join(f'/homes/users/hlindstadt/gonzalez_lab/CNV/liftoff/{folder}', filename)) as f:
                                        global df
                                        df = pd.read_csv(f, sep='\t', header=None)
                                        print(f"{filename}: started")
                                        print(f"{filename}: finished")
                                        process_file(filename, df)

def process_file(filename, df):
# make columns, name columns, drop columns, and drop all but genes
        df.columns=['chromosome','source','feature','start','end','Xscore','strand','Xframe','attributes']
        df.drop(df[df.feature != 'gene'].index, inplace=True)
        df = df.drop(df[~df['seqname'].isin(['X', '3L','3R', '2L','2R','4'])].index)
        try:
                df[['gene id','name','coverage','seqID','copy number','5','6','7','8']]= df.attributes.str.split(";",expand=True,)
        except:
                df[['gene id','name','coverage','seqID','copy number','5','6','7','8','9']]= df.attributes.str.split(";",expand=True,)
                df= df.drop(['9'], axis=1)
                print('expansion error, expanded to 9')

        df['length']=df['end']-df['start']
        df= df.drop(['start','source','attributes','feature','strand','end','Xscore','Xframe','5','6','7','8'], axis=1)

# clean up the names of entries in the dataframe
        df['gene id'] = df['gene id'].str.replace('gene_id ','')
        df['gene id'] = df['gene id'].str.replace('"','')

        df['name'] = df['name'].str.replace('gene_symbol ','')
        df['name'] = df['name'].str.replace('"','')

        df['coverage'] = df['coverage'].str.replace('coverage ','')
        df['coverage'] = df['coverage'].str.replace('"','')

        df['seqID'] = df['seqID'].str.replace('sequence_ID ','')
        df['seqID'] = df['seqID'].str.replace('"','')

        df['copy number'] = df['copy number'].str.replace('extra_copy_number ','')
        df['copy number'] = df['copy number'].str.replace('"','')

        df.loc[df['coverage'] == ' Parent ', 'seqID'] = 0
        df.loc[df['coverage'] == ' Parent ', 'copy number'] = 0
        df.loc[df['coverage'] == ' Parent ', 'coverage'] = 0

        df['coverage'] = pd.to_numeric(df['coverage'], downcast="float")
        df['seqID'] = pd.to_numeric(df['seqID'], downcast="float")

        df.loc[(df['coverage'] > 0.79), 'coverage'] = 'Yes'
        df.loc[(df['coverage'] != 'Yes'), 'coverage'] = 'No'

        df.loc[(df['seqID'] > 0.79), 'seqID'] = 'Yes'
        df.loc[(df['seqID'] != 'Yes'), 'seqID'] = 'No'
        print("finished")

        df.to_csv(f'{filename}_sum.csv', index=False)
        os.system(f'cd ..')



def run():
        read_in_reff()

run()
