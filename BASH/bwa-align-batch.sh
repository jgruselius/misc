#!/bin/bash -l

#SBATCH -A b2013064
#SBATCH -p node
#SBATCH -n 1
#SBATCH -e bwa-align-batch-%j.err
#SBATCH -o bwa-align-batch-%j.out
#SBATCH --mail-user joel.gruselius@scilifelab.se
#SBATCH --mail-type=ALL

DATA_DIR=/proj/b2013064/nobackup/joel
REF=/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/bwa/hg19.fa

module load bioinfo-tools
module load samtools 
module load bwa

#time samtools faidx $REF
#time bwa index $REF

sep="\n"
echo -e "REFERENCE FILE:\n$REF"
echo -e "OUTPUT DIR:\n$DATA_DIR/aln/"
echo "FILES:"
for file in "$@";do echo "$(basename $file)";done
echo -e $sep

files="$@"
for file in ${files[@]}
do
	echo -e "INPUT:\n$(readlink -e $file)"
	echo -e "OUTPUT:\n$DATA_DIR/aln/$(basename ${file%fastq.gz})sai"
	time bwa aln -t 8 $REF $(readlink $file) > $DATA_DIR/aln/$(basename ${file%fastq.gz})sai
	echo -e $sep
done
