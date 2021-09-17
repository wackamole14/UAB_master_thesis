import pandas as pd
import os

#filename=sys.argv[1]

def read_in_reff():
# import the bounaries csv or make the first one        
        read_single='no'
        if os.path.exists('boundaries_summary.csv'):
                df_1= pd.read_csv("boundaries_summary.csv", sep=',')
        else:
                df_1 = pd.DataFrame(columns=['sample','2L','2R','3L','3R','X'])

        for filename in os.listdir('/homes/users/hlindstadt/scratch/liftoff/Boundaries'):
                if filename.endswith('.csv'):
                        with open(os.path.join(f'/homes/users/hlindstadt/scratch/liftoff/Boundaries', filename)) as f:
                                df = pd.read_csv(f, sep=',')
                                print(f"{filename}: started")
                                process_file(filename, df, df_1, read_single)
def read_single():
        read_single='yes'
        df_1 = pd.DataFrame(columns=['sample','2L','2R','3L','3R','X'])
        with open(os.path.join(f'/homes/users/hlindstadt/scratch/liftoff/Boundaries', filename)) as f:
                                df = pd.read_csv(f, sep=',')
                                print(f"{filename}: started")
                                process_file(filename, df, df_1)
###

def process_file(filename, df, df_1, read_single):
        df_1.reset_index(drop=True, inplace=True)

# loop through the chromosomes and calculate the distances 
        chromosomes= ['2L','2R','3L','3R','X']
        number = 0
        series=[filename,]
        for chromosome in chromosomes:
                series.append(df['end'].iloc[number+1] - df['start'].iloc[number])
                number += 2
# add new rom to the dataframe
        df_1.loc[-1] = series
        print(f'{filename} processed')
# overwrite old bounaries file with new row
        df_1.reset_index(drop=True, inplace=True)

        df_1['sample'] = df_1['sample'].str.replace('boundaries_','')
        df_1['sample'] = df_1['sample'].str.replace('_liftoff.csv','')
        if read_single=='yes':
                df_1.to_csv(f'boundaries_summ_{filename}.csv')
        else:
                df_1.to_csv('boundaries_summary.csv')


def run():
        #read_single()
        read_in_reff()
        
run()
