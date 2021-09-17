import pandas as pd
import os
import sys

# give path to the boundaries files.

path=sys.argv[1]

def read_in_reff():
        for filename in os.listdir(path):
                if filename.endswith('_liftoff.csv'):
                        with open(os.path.join(path, filename)) as f:
                                df = pd.read_csv(f, sep=',')
                                bounds,name,liftoff= filename.split('_')
                                print(f"{name}: started")
                                process_file(filename, df, name)

def process_file(filename, df, name):
        chromosomes= ['2L','2R','3L','3R','X']
        number = 0
        series=[]
        for chromosome in chromosomes:
                series.append(chromosome)
                series.append(df['start'].iloc[number])
                series.append(df['end'].iloc[number+1])
                number += 2
        series = [series[x:x+3] for x in range(0, len(series), 3)]
        df = pd.DataFrame(data=series)
        os.system(f'cd /homes/users/hlindstadt/scratch/Boundaries/Bounds')
        df.to_csv(f'bounds_{name}', header=None, index=None)

def run():
        read_in_reff()

run()
