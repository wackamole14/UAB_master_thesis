#!/bin/sh
#SBATCH --partition=normal
#SBATCH --cpus-per-task=1
#SBATCH --mem=32000
#SBATCH --mail-type=ALL
#SBATCH --job-name=failed_sample_1
#SBATCH --output=failed_sample_1.out 
#SBATCH --error=failed_sample_1.err 
#SBATCH --mail-user=hannah.kay.lindstadt@gmail.com


SAMPLE_PATH=(/homes/users/hlindstadt/gonzalez_lab/CNV/Assemblies/1_hide/COR018.fa)
FILE="$(basename "$SAMPLE_PATH" .fa)"

REFF_PATH=/homes/users/hlindstadt/gonzalez_lab/CNV/Assemblies/iso_v31_genome.fasta

mkdir $FILE
cd $FILE


/homes/users/hlindstadt/gonzalez_lab/CNV/Scripts/svmu/svmu ${FILE}2ISO.mm.delta $REFF_PATH $SAMPLE_PATH l ${FILE}_lastz.txt $FILE

cd ..
