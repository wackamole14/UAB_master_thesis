import os   #os should be installled with python version in miniconda

processed = 0


def read_in_reff():
        df_reff = pd.read_csv('reff_summary.csv')
        for filename in os.listdir('/homes/users/hlindstadt/scratch/summary_liftoff'):
                if filename.endswith('_liftoff_sum.csv'):
                        with open(os.path.join(f'/homes/users/hlindstadt/scratch/summary_liftoff', filename)) as f:
                                df = pd.read_csv(f)
                                print(f"{filename}: started")
                                process_file(filename, df, df_reff)

def process_file(filename, df, df_reff):
        global processed
# this will switch the compard file to be the latest one, to not overwrite the reff file.       
        if processed !=0:
                df_reff= pd.read_csv('reff_summary_1.csv')
# tidy the column names and add necessary columns       
        df= df.drop(['seqname','name','length'], axis=1)
        df.insert(1, 'reff length', 0)

        df.loc[(df['gene id'].duplicated() == False), 'absent'] = 1
        df.loc[(df['gene id'].duplicated() == True), 'absent'] = 0

        df['summary']= 0
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
# concat the dataframes 
        frames=[df_reff,df]
        concat = pd.concat(frames)
        reff_summary = concat.groupby(['gene id']).sum()
        reff_summary.sort_values(by=['reff length'])
# overwrite old combined file and switch to new file for next process run
        processed += 1
        reff_summary.to_csv('reff_summary_1.csv')

def run():
        read_in_reff()
run()
