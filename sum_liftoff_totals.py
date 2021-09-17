/bin/env python

import pandas as pd
import os

def read_in_ref():
# import the bounaries csv or make the first one
        for filename in os.listdir('/homes/users/hlindstadt/scratch/summary_liftoff/process'):
                if filename.endswith('_liftoff_sum.csv'):
                        with open(os.path.join(f'/homes/users/hlindstadt/scratch/summary_liftoff/process', filename)) as f:
                                df = pd.read_csv(f, sep=',')
                                process_files(filename, df)


def process_files(filename,df):
        data = {'Total genes': [0],'Total CNV': [0],'Total lacking coverage': [0],'Total lacking seqID': [0]}
        df_new = pd.DataFrame(data,columns=['Sample','Total genes','Total CNV','Total lacking seqID','Total lacking coverage'])

        filename,liftoff,summary= filename.split('_')

        print(f"{filename}: started")
        df_new['Sample']= filename

        cnvs = df['copy number'].value_counts()
        df_new['Total CNV'] = cnvs[1]

        seqid = df['seqID'].value_counts()
        df_new['Total lacking seqID'] = seqid[1]

        coverage = df['coverage'].value_counts()
        df_new['Total lacking coverage'] = coverage[1]

        df_new['Total genes']= len(df)

        if os.path.exists('liftoff_summary.csv'):
                df_sum= pd.read_csv("liftoff_summary.csv", sep=',')
                df= pd.concat([df_new, df_sum])
                df.to_csv('liftoff_summary.csv', index=False)
        else:
                df_new.to_csv('liftoff_summary.csv', index=False)

def run():
        read_in_ref()

run()
