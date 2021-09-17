#!/bin/sh
#SBATCH --partition=normal
#SBATCH --cpus-per-task=1
#SBATCH --mem=15000
#SBATCH --mail-type=ALL
#SBATCH --job-name=SV_Analysis
#SBATCH --output=SV_Analysis.out 
#SBATCH --error=SV_Analysis.err 
#SBATCH --mail-user=hannah.kay.lindstadt@gmail.com

module load Miniconda3/4.7.10
source activate /homes/users/hlindstadt/.conda/envs/SV_Analysis


# can add the name of the files you want here, in the SAMPLES list. 

FILE_PATH=/homes/users/hlindstadt/gonzalez_lab/CNV/
SAMPLES=(B59 ZH26 I23 T29A N25)


for FILE in "${SAMPLES[@]}"
do
#FILE="$(basename "$SAMPLES")"
python /homes/users/hlindstadt/gonzalez_lab/CNV/SV_Analysis.py $FILE_PATH $FILE
done






# packages in environment at /homes/aplic/noarch/software/Miniconda3/4.7.10:
#
# Name                    Version                   Build  Channel
# _libgcc_mutex             0.1                        main  
# _r-mutex                  1.0.1               anacondar_1    conda-forge
# apbs                      1.5                  h14c3975_3    schrodinger
# asn1crypto                0.24.0                   py37_0  
# binutils_impl_linux-64    2.34                 h53a641e_0    conda-forge
# binutils_linux-64         2.34                hc952b39_18    conda-forge
# biopython                 1.78             py37h4abf009_1    conda-forge
# bwidget                   1.9.14                        0    conda-forge
# bzip2                     1.0.8                h7b6447c_0  
# ca-certificates           2020.12.5            ha878542_0    conda-forge
# cairo                     1.14.12              h8948797_3  
# certifi                   2020.12.5        py37h89c1867_1    conda-forge
# cffi                      1.12.3           py37h2e261b9_0  
# chardet                   3.0.4                    py37_1  
# collada2gltf              2.1.4                h6bb024c_0    schrodinger
# conda                     4.9.2            py37h89c1867_0    conda-forge
# conda-package-handling    1.3.11                   py37_0  
# cryptography              2.7              py37h1ba5d50_0  
# curl                      7.68.0               hf8cf82a_0    conda-forge
# cycler                    0.10.0                   pypi_0    pypi
# dbus                      1.13.6               he372182_0    conda-forge
# edlib                     1.3.8.post2              pypi_0    pypi
# expat                     2.2.10               he6710b0_2  
# fontconfig                2.13.0               h9420a91_0  
# freemol                   1.158                      py_2    schrodinger
# freetype                  2.10.4               h7ca028e_0    conda-forge
# fribidi                   1.0.5             h516909a_1002    conda-forge
# future                    0.18.2           py37hc8dfbb8_1    conda-forge
# gcc_impl_linux-64         7.3.0                habb00fd_1  
# gcc_linux-64              7.3.0               h553295d_18    conda-forge
# gettext                   0.19.8.1          hc5be6a0_1002    conda-forge
# gfortran_impl_linux-64    7.3.0                hdf63c60_5    conda-forge
# gfortran_linux-64         7.3.0               h553295d_18    conda-forge
# glew                      2.0.0                         0    schrodinger
# glib                      2.58.3          py37he00f558_1003    conda-forge
# graphite2                 1.3.13            he1b5a44_1001    conda-forge
# gsl                       2.4               h294904e_1006    conda-forge
# gst-plugins-base          1.14.5               h0935bb2_2    conda-forge
# gstreamer                 1.14.5               h36ae1b5_2    conda-forge
# gxx_impl_linux-64         7.3.0                hdf63c60_1  
# gxx_linux-64              7.3.0               h553295d_18    conda-forge
# h5py                      2.10.0          nompi_py37h513d04c_102    conda-forge
# harfbuzz                  1.8.8                hffaf4a1_0  
# hdf4                      4.2.13            hf30be14_1003    conda-forge
# hdf5                      1.10.5          nompi_h3c11f04_1104    conda-forge
# icu                       58.2              hf484d3e_1000    conda-forge
# idna                      2.8                      py37_0  
# jinja2                    2.11.1                     py_0    conda-forge
# jpeg                      9c                h14c3975_1001    conda-forge
# kiwisolver                1.3.1                    pypi_0    pypi
# krakentools               0.1                        py_0    bioconda
# krb5                      1.16.4               h173b8e3_0  
# lcms2                     2.11                 h396b838_0  
# ld_impl_linux-64          2.34                 h53a641e_0    conda-forge
# libarchive                3.3.3                h5d8350f_5  
# libblas                   3.8.0               14_openblas    conda-forge
# libcblas                  3.8.0               14_openblas    conda-forge
# libcurl                   7.68.0               hda55be3_0    conda-forge
# libedit                   3.1.20181209         hc058e9b_0  
# libffi                    3.2.1                hd88cf55_4  
# libgcc-ng                 9.1.0                hdf63c60_0  
# libgfortran-ng            7.3.0                hdf63c60_5    conda-forge
# libglu                    9.0.0             he1b5a44_1001    conda-forge
# libholoplaycore           0.1.0_rc4                     1    schrodinger
# libiconv                  1.15              h516909a_1006    conda-forge
# liblapack                 3.8.0               14_openblas    conda-forge
# libnetcdf                 4.7.4           nompi_h9f9fd6a_101    conda-forge
# libopenblas               0.3.7                h5ec1e0e_6    conda-forge
# libpng                    1.6.37               hed695b0_1    conda-forge
# libssh2                   1.8.2                h22169c7_2    conda-forge
# libstdcxx-ng              9.1.0                hdf63c60_0  
# libtiff                   4.1.0                h2733197_0  
# libuuid                   1.0.3                h1bed415_2  
# libxcb                    1.13              h14c3975_1002    conda-forge
# libxml2                   2.9.9                hea5a465_1  
# lz4-c                     1.8.3             he1b5a44_1001    conda-forge
# lzo                       2.10                 h49e0be7_2  
# make                      4.3                  h516909a_0    conda-forge
# mappy                     2.17             py37h84994c4_0    bioconda
# markupsafe                1.1.1            py37h8f50634_1    conda-forge
# matplotlib                3.4.2                    pypi_0    pypi
# mengine                   1                    h14c3975_1    schrodinger
# mpeg_encode               1                    h14c3975_1    schrodinger
# mtz2ccp4_px               1.0                  h9ac9557_3    schrodinger
# ncurses                   6.1                  he6710b0_1  
# numpy                     1.18.1           py37h95a1406_0    conda-forge
# olefile                   0.46               pyh9f0ad1d_1    conda-forge
# ont-tombo                 1.5.1           py37r36hb3f55d8_0    bioconda
# openssl                   1.1.1e               h516909a_0    conda-forge
# pandas                    1.2.4                    pypi_0    pypi
# pango                     1.42.4               h049681c_0  
# pcre                      8.44                 he1b5a44_0    conda-forge
# pdb2pqr                   2.1.2+pymol                py_0    schrodinger
# pillow                    8.1.0            py37he98fc37_0  
# pip                       19.1.1                   py37_0  
# pixman                    0.38.0            h516909a_1003    conda-forge
# pmw                       2.0.1+3                    py_3    schrodinger
# pthread-stubs             0.4               h14c3975_1001    conda-forge
# pycollada                 0.6                        py_0    schrodinger
# pycosat                   0.6.3            py37h14c3975_0  
# pycparser                 2.19                     py37_0  
# pyfaidx                   0.5.8                      py_1    bioconda
# pykerberos                1.2.1            py37h89bfc95_1    conda-forge
# pymol                     2.4.1            py37h913975d_0    schrodinger
# pymol-bundle              2.4.1                         0    schrodinger
# pymol-web-examples        2.4                           1    schrodinger
# pyopenssl                 19.0.0                   py37_0  
# pyparsing                 3.0.0b2                  pypi_0    pypi
# pyqt                      5.9.2            py37hcca6a23_4    conda-forge
# pysam                     0.16.0.1                 pypi_0    pypi
# pysocks                   1.7.0                    py37_0  
# python                    3.7.3                h0371630_0  
# python-dateutil           2.8.1                      py_0    conda-forge
# python-libarchive-c       2.8                     py37_11  
# python_abi                3.7                     1_cp37m    conda-forge
# pytz                      2019.3                     py_0    conda-forge
# qt                        5.9.7                h5867ecd_1  
# r-assertthat              0.2.1             r36h6115d3f_1    conda-forge
# r-backports               1.1.5             r36hcdcec82_0    conda-forge
# r-base                    3.6.1                h9bb98a2_1  
# r-callr                   3.4.2             r36h6115d3f_0    conda-forge
# r-cli                     2.0.2             r36h6115d3f_0    conda-forge
# r-colorspace              1.4_1             r36hcdcec82_1    conda-forge
# r-crayon                  1.3.4           r36h6115d3f_1002    conda-forge
# r-desc                    1.2.0           r36h6115d3f_1002    conda-forge
# r-digest                  0.6.25            r36h0357c0b_0    conda-forge
# r-ellipsis                0.3.0             r36hcdcec82_0    conda-forge
# r-evaluate                0.14              r36h6115d3f_1    conda-forge
# r-fansi                   0.4.1             r36hcdcec82_0    conda-forge
# r-farver                  2.0.3             r36h0357c0b_0    conda-forge
# r-ggplot2                 3.3.0             r36h6115d3f_0    conda-forge
# r-glue                    1.3.2             r36hcdcec82_0    conda-forge
# r-gridextra               2.3             r36h6115d3f_1002    conda-forge
# r-gtable                  0.3.0             r36h6115d3f_2    conda-forge
# r-isoband                 0.2.0             r36h0357c0b_0    conda-forge
# r-labeling                0.3             r36h6115d3f_1002    conda-forge
# r-lattice                 0.20_40           r36hcdcec82_0    conda-forge
# r-lifecycle               0.2.0             r36h6115d3f_0    conda-forge
# r-magrittr                1.5             r36h6115d3f_1002    conda-forge
# r-mass                    7.3_51.5          r36hcdcec82_0    conda-forge
# r-matrix                  1.2_18            r36h7fa42b6_2    conda-forge
# r-mgcv                    1.8_31            r36h7fa42b6_0    conda-forge
# r-munsell                 0.5.0           r36h6115d3f_1002    conda-forge
# r-nlme                    3.1_145           r36h9bbef5b_0    conda-forge
# r-pillar                  1.4.3             r36h6115d3f_0    conda-forge
# r-pkgbuild                1.0.6             r36h6115d3f_0    conda-forge
# r-pkgconfig               2.0.3             r36h6115d3f_0    conda-forge
# r-pkgload                 1.0.2           r36h0357c0b_1001    conda-forge
# r-praise                  1.0.0           r36h6115d3f_1003    conda-forge
# r-prettyunits             1.1.1             r36h6115d3f_0    conda-forge
# r-processx                3.4.2             r36hcdcec82_0    conda-forge
# r-ps                      1.3.2             r36hcdcec82_0    conda-forge
# r-r6                      2.4.1             r36h6115d3f_0    conda-forge
# r-rcolorbrewer            1.1_2           r36h6115d3f_1002    conda-forge
# r-rcpp                    1.0.4             r36h0357c0b_0    conda-forge
# r-rlang                   0.4.5             r36hcdcec82_0    conda-forge
# r-rprojroot               1.3_2           r36h6115d3f_1002    conda-forge
# r-rstudioapi              0.11              r36h6115d3f_0    conda-forge
# r-scales                  1.1.0             r36h6115d3f_0    conda-forge
# r-testthat                2.3.2             r36h0357c0b_0    conda-forge
# r-tibble                  2.1.3             r36hcdcec82_1    conda-forge
# r-utf8                    1.1.4           r36hcdcec82_1001    conda-forge
# r-vctrs                   0.2.4             r36hcdcec82_0    conda-forge
# r-viridislite             0.3.0           r36h6115d3f_1002    conda-forge
# r-withr                   2.1.2           r36h6115d3f_1001    conda-forge
# r-zeallot                 0.1.0           r36h6115d3f_1001    conda-forge
# readline                  7.0                  h7b6447c_5  
# requests                  2.22.0                   py37_0  
# rigimol                   1.3                           2    schrodinger
# rpy2                      3.1.0           py37r36hc1659b7_3    conda-forge
# ruamel_yaml               0.15.46          py37h14c3975_0  
# scipy                     1.4.1            py37h921218d_0    conda-forge
# seaborn                   0.11.1                   pypi_0    pypi
# setuptools                41.0.1                   py37_0  
# simplegeneric             0.8.1                      py_1    conda-forge
# sip                       4.19.8           py37hf484d3e_0  
# six                       1.12.0                   py37_0  
# sqlite                    3.29.0               h7b6447c_0  
# tk                        8.6.8                hbc83047_0  
# tktable                   2.10                 h14c3975_0  
# tqdm                      4.32.1                     py_0  
# tzlocal                   2.0.0                      py_0    conda-forge
# umi-amplicon-tools        1.0.0                    pypi_0    pypi
# urllib3                   1.24.2                   py37_0  
# wheel                     0.33.4                   py37_0  
# xorg-libxau               1.0.9                h14c3975_0    conda-forge
# xorg-libxdmcp             1.1.3                h516909a_0    conda-forge
# xz                        5.2.4                h14c3975_4  
# yaml                      0.1.7                had09818_2  
# zlib                      1.2.11               h7b6447c_3  
# zstd                      1.3.7                h0b5b093_0  
