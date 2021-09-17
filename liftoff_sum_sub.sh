#!/bin/sh
#SBATCH --partition=normal
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000
#SBATCH --mail-type=ALL
#SBATCH --job-name=liftoff_summary
#SBATCH --output=liftoff_sum.out 
#SBATCH --error=liftoff_sum.err 
#SBATCH --mail-user=hannah.kay.lindstadt@gmail.com


module load Miniconda3/4.7.10

source activate /homes/users/hlindstadt/.conda/envs/liftoff_summary

python 1_liftoff_sum.py





# packages in environment at /homes/users/hlindstadt/.conda/envs/liftoff_summary:
#
# Name                    Version                   Build  Channel
# _libgcc_mutex             0.1                        main  
# blas                      1.0                         mkl  
# ca-certificates           2021.1.19            h06a4308_1  
# certifi                   2020.12.5        py38h06a4308_0  
# intel-openmp              2020.2                      254  
# ld_impl_linux-64          2.33.1               h53a641e_7  
# libffi                    3.3                  he6710b0_2  
# libgcc-ng                 9.1.0                hdf63c60_0  
# libstdcxx-ng              9.1.0                hdf63c60_0  
# mkl                       2020.2                      256  
# mkl-service               2.3.0            py38he904b0f_0  
# mkl_fft                   1.3.0            py38h54f3939_0  
# mkl_random                1.1.1            py38h0573a6f_0  
# ncurses                   6.2                  he6710b0_1  
# numpy                     1.19.2           py38h54aff64_0  
# numpy-base                1.19.2           py38hfa32c7d_0  
# openssl                   1.1.1k               h27cfd23_0  
# pandas                    1.2.3            py38ha9443f7_0  
# pip                       21.0.1           py38h06a4308_0  
# python                    3.8.8                hdb3f193_4  
# python-dateutil           2.8.1              pyhd3eb1b0_0  
# pytz                      2021.1             pyhd3eb1b0_0  
# readline                  8.1                  h27cfd23_0  
# setuptools                52.0.0           py38h06a4308_0  
# six                       1.15.0           py38h06a4308_0  
# sqlite                    3.35.4               hdfb4753_0  
# tk                        8.6.10               hbc83047_0  
# wheel                     0.36.2             pyhd3eb1b0_0  
# xz                        5.2.5                h7b6447c_0  
# zlib                      1.2.11               h7b6447c_3 