#!/bin/sh
#SBATCH --partition=normal
#SBATCH --nodelist=mr-05-02 
#SBATCH --cpus-per-task=5
#SBATCH --mem=800000
#SBATCH --mail-type=ALL
#SBATCH --job-name=CNV2VCF_fix
#SBATCH --output=CNV2VCF_fix_4.out 
#SBATCH --error=CNV2VCF_fix_4.err 
#SBATCH --mail-user=hannah.kay.lindstadt@gmail.com

module load Miniconda3/4.7.10

source activate /homes/users/hlindstadt/.conda/envs/CNV2VCF

python ./TOOLS/CNV2VCF.py comSplitter.out id_file.txt locusseq ./TOOLS/CutTree.R > ALL_SV_results.VCF


# packages in environment at /homes/users/hlindstadt/.conda/envs/CNV2VCF:
#
# # Name                    Version                   Build  Channel
# _libgcc_mutex             0.1                        main  
# _r-mutex                  1.0.0               anacondar_1  
# blas                      1.0                         mkl  
# bzip2                     1.0.8                h7b6447c_0  
# ca-certificates           2021.5.25            h06a4308_1  
# cairo                     1.14.12              h8948797_3  
# certifi                   2021.5.30        py37h06a4308_0  
# clustalo                  1.2.3                         0    bioconda
# curl                      7.69.1               hbc83047_0  
# fontconfig                2.13.1               h6c09931_0  
# freetype                  2.10.4               h5ab3b9f_0  
# fribidi                   1.0.10               h7b6447c_0  
# glib                      2.63.1               h5a9c865_0  
# graphite2                 1.3.14               h23475e2_0  
# harfbuzz                  1.8.8                hffaf4a1_0  
# htslib                    1.9                  h4da6232_3    bioconda
# icu                       58.2                 he6710b0_3  
# intel-openmp              2021.2.0           h06a4308_610  
# jpeg                      9b                   h024ee3a_2  
# krb5                      1.17.1               h173b8e3_0  
# ld_impl_linux-64          2.33.1               h53a641e_7    anaconda
# libcurl                   7.69.1               h20c2e04_0  
# libdeflate                1.2                  h516909a_1    bioconda
# libedit                   3.1.20181209         hc058e9b_0  
# libffi                    3.2.1             hf484d3e_1007  
# libgcc                    7.2.0                h69d50b8_2  
# libgcc-ng                 9.1.0                hdf63c60_0  
# libpng                    1.6.37               hbc83047_0  
# libssh2                   1.9.0                h1ba5d50_1  
# libstdcxx-ng              9.1.0                hdf63c60_0  
# libtiff                   4.1.0                h2733197_1  
# libuuid                   1.0.3                h1bed415_2  
# libxcb                    1.14                 h7b6447c_0  
# libxml2                   2.9.10               hb55368b_3  
# lz4-c                     1.9.3                h2531618_0  
# mkl                       2021.2.0           h06a4308_296  
# mkl-service               2.3.0            py37h27cfd23_1  
# mkl_fft                   1.3.0            py37h42c9631_2  
# mkl_random                1.2.1            py37ha9443f7_2  
# ncurses                   6.1                  he6710b0_1  
# numpy                     1.20.2           py37h2d18471_0  
# numpy-base                1.20.2           py37hfae3a4d_0  
# openssl                   1.1.1k               h27cfd23_0  
# pandas                    1.2.4            py37h2531618_0  
# pango                     1.42.4               h049681c_0  
# pcre                      8.44                 he6710b0_0  
# pip                       20.2.4                   py37_0    anaconda
# pixman                    0.40.0               h7b6447c_0  
# python                    3.7.6                h0371630_2  
# python-dateutil           2.8.1              pyhd3eb1b0_0  
# pytz                      2021.1             pyhd3eb1b0_0  
# r                         3.2.2                         0  
# r-ade4                    1.7_2                  r3.2.2_0    bioconda
# r-base                    3.2.2                         0  
# r-boot                    1.3_17                r3.2.2_0a  
# r-class                   7.3_14                r3.2.2_0a  
# r-cluster                 2.0.3                 r3.2.2_0a  
# r-codetools               0.2_14                r3.2.2_0a  
# r-foreign                 0.8_66                r3.2.2_0a  
# r-kernsmooth              2.23_15               r3.2.2_0a  
# r-lattice                 0.20_33               r3.2.2_0a  
# r-mass                    7.3_45                r3.2.2_0a  
# r-matrix                  1.2_2                 r3.2.2_0a  
# r-mgcv                    1.8_9                 r3.2.2_0a  
# r-nlme                    3.1_122               r3.2.2_0a  
# r-nnet                    7.3_11                r3.2.2_0a  
# r-recommended             3.2.2                  r3.2.2_0  
# r-rpart                   4.1_10                r3.2.2_0a  
# r-seqinr                  3.1_3                  r3.2.2_0    bioconda
# r-spatial                 7.3_11                r3.2.2_0a  
# r-survival                2.38_3                r3.2.2_0a  
# readline                  7.0                  h7b6447c_5  
# samtools                  1.9                 h10a08f8_12    bioconda
# setuptools                50.3.0           py37hb0f4dca_1    anaconda
# six                       1.16.0             pyhd3eb1b0_0  
# sqlite                    3.31.1               h7b6447c_0  
# tk                        8.6.10               hbc83047_0    anaconda
# wheel                     0.35.1                     py_0    anaconda
# xz                        5.2.5                h7b6447c_0  
# zlib                      1.2.11               h7b6447c_3  
# zstd                      1.4.9                haebb681_0  
