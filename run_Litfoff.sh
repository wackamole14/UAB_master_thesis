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
~     
