#!/bin/sh
#SBATCH --partition=normal
#SBATCH --cpus-per-task=6
#SBATCH --mem=10000
#SBATCH --mail-type=ALL
#SBATCH --job-name=ALL_liftoff
#SBATCH --output=ALL_liftoff_%A_%a.out 
#SBATCH --error=ALL_liftoff_%A_%a.err 
#SBATCH --mail-user=hannah.kay.lindstadt@gmail.com
#SBATCH --array=0-49

FILE_LIST=(/homes/users/hlindstadt/gonzalez_lab/CNV/Assemblies/*.fa)
FILE="${FILE_LIST[$SLURM_ARRAY_TASK_ID]}"
FILE_NAME=$(basename "$FILE" .fa)

REF_GFT=/homes/users/hlindstadt/gonzalez_lab/CNV/dmel-all-r6.31.gtf

REF=/homes/users/hlindstadt/gonzalez_lab/CNV/dmel-all-chromosome-r6.31.fasta

mkdir ${FILE_NAME}

cd ${FILE_NAME}

module load Miniconda3/4.7.10
source /homes/aplic/noarch/software/Miniconda3/4.7.10/etc/profile.d/conda.sh
conda activate Liftoff_Processing

liftoff -copies -p 6 -o ${FILE_NAME}_liftoff -u ${FILE_NAME}_unmapped -g $REF_GFT $FILE $REF

cd ..






# packages in environment at /homes/users/hlindstadt/.conda/envs/Liftoff_Processing:
#
# Name                    Version                   Build  Channel
# _libgcc_mutex             0.1                 conda_forge    conda-forge
# _openmp_mutex             4.5                       1_gnu    conda-forge
# argcomplete               1.12.2             pyhd8ed1ab_0    conda-forge
# argh                      0.26.2          pyh9f0ad1d_1002    conda-forge
# biopython                 1.78             py36h8f6f2f9_2    conda-forge
# bzip2                     1.0.8                h7f98852_4    conda-forge
# c-ares                    1.17.1               h7f98852_1    conda-forge
# ca-certificates           2021.1.19            h06a4308_1  
# certifi                   2020.12.5        py36h5fab9bb_1    conda-forge
# decorator                 4.4.2                      py_0    conda-forge
# gffutils                  0.10.1             pyh864c0ab_1    bioconda
# importlib-metadata        3.10.0           py36h5fab9bb_0    conda-forge
# importlib_metadata        3.10.0               hd8ed1ab_0    conda-forge
# interlap                  0.2.7              pyh9f0ad1d_0    conda-forge
# k8                        0.2.5                h9a82719_1    bioconda
# krb5                      1.17.2               h926e7f8_0    conda-forge
# ld_impl_linux-64          2.35.1               hea4e1c9_2    conda-forge
# libblas                   3.9.0                8_openblas    conda-forge
# libcblas                  3.9.0                8_openblas    conda-forge
# libcurl                   7.75.0               hc4aaa36_0    conda-forge
# libdeflate                1.7                  h7f98852_5    conda-forge
# libedit                   3.1.20191231         he28a2e2_2    conda-forge
# libev                     4.33                 h516909a_1    conda-forge
# libffi                    3.3                  h58526e2_2    conda-forge
# libgcc-ng                 9.3.0               h2828fa1_18    conda-forge
# libgfortran-ng            9.3.0               hff62375_18    conda-forge
# libgfortran5              9.3.0               hff62375_18    conda-forge
# libgomp                   9.3.0               h2828fa1_18    conda-forge
# liblapack                 3.9.0                8_openblas    conda-forge
# libnghttp2                1.43.0               h812cca2_0    conda-forge
# libopenblas               0.3.12          pthreads_h4812303_1    conda-forge
# libssh2                   1.9.0                ha56f1ee_6    conda-forge
# libstdcxx-ng              9.3.0               h6de172a_18    conda-forge
# liftoff                   1.5.2                      py_0    bioconda
# minimap2                  2.17                 h5bf99c6_4    bioconda
# ncurses                   6.2                  h58526e2_4    conda-forge
# networkx                  2.5                        py_0    conda-forge
# numpy                     1.19.5           py36h2aa4a07_1    conda-forge
# openssl                   1.1.1k               h7f98852_0    conda-forge
# pip                       21.0.1             pyhd8ed1ab_0    conda-forge
# pyfaidx                   0.5.9.5            pyh3252c3a_0    bioconda
# pysam                     0.16.0.1         py36h61e5637_3    bioconda
# python                    3.6.13          hffdb5ce_0_cpython    conda-forge
# python_abi                3.6                     1_cp36m    conda-forge
# readline                  8.0                  he28a2e2_2    conda-forge
# setuptools                49.6.0           py36h5fab9bb_3    conda-forge
# simplejson                3.8.1                    py36_0    bioconda
# six                       1.15.0             pyh9f0ad1d_0    conda-forge
# sqlite                    3.35.3               h74cdb3f_0    conda-forge
# tk                        8.6.10               h21135ba_1    conda-forge
# typing_extensions         3.7.4.3                    py_0    conda-forge
# ujson                     4.0.2            py36hc4f0c31_0    conda-forge
# wheel                     0.36.2             pyhd3deb0d_0    conda-forge
# xz                        5.2.5                h516909a_1    conda-forge
# zipp                      3.4.1              pyhd8ed1ab_0    conda-forge
# zlib                      1.2.11            h516909a_1010    conda-forge

~     
