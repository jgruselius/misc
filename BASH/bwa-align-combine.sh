#!/bin/bash -l

#SBATCH -A b2013064
#SBATCH -p node
#SBATCH -n 1
#SBATCH -e bwa-align-combine-%j.err
#SBATCH -o bwa-align-combine-%j.out
#SBATCH --mail-user joel.gruselius@scilifelab.se
#SBATCH --mail-type=ALL

DATA_DIR=/proj/b2013064/nobackup/joel
REF=/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/bwa/hg19.fa

module load bioinfo-tools
module load bwa
module load samtools

sep="\n"
echo -e "REFERENCE FILE:\n$REF"
echo -e "OUTPUT DIR:\n$DATA_DIR/aln/"
echo "INPUT FILES:"
for file in "$@";do echo "$(basename $file)";done
echo -e $sep

files="$@"
for file in ${files[@]}
do
	filebase=$(basename $file)
	read2file=${file/_1.fastq/_2.fastq}
	readid=${filebase%_1.fastq.gz}
	read1sai=$DATA_DIR/aln/$readid"_1.sai"
	read2sai=$DATA_DIR/aln/$readid"_2.sai"
	# Do only for read 1 files:
	if [ ${file:(-11):2} == "_1" ]; then
		# Check that all files exists:
		if [ -e $file -a -e $read2file -a -e $read1sai -a -e $read2sai ]; then
			echo "INPUT:"
			echo -e "READ 1 FASTQ:\n$(readlink -e $file)"
			echo -e "READ 1 ALNGM:\n$read1sai"
			echo -e "READ 2 FASTQ:\n$(readlink -e $read2file)"
			echo -e "READ 2 ALNGM:\n$read2sai"
			echo -e "OUTPUT:\n$DATA_DIR/aln/$readid.sam"
			#time bwa sampe -P $REF $read1sai $read2sai $(readlink -e $file) $(readlink -e $read2file) > $DATA_DIR/aln/$readid.sam
			# Merge reads, convert to BAM, sort and index:
			time bwa sampe -P $REF $read1sai $read2sai $(readlink -e $file) $(readlink -e $read2file) | samtools view -Shb - > $DATA_DIR/aln/$readid.unsorted.bam && rm -f $read1sai $read2sai
			time samtools sort $DATA_DIR/aln/$readid.unsorted.bam $DATA_DIR/aln/$readid && rm -f $DATA_DIR/aln/$readid.unsorted.bam
			time samtools index $DATA_DIR/aln/$readid.bam
			time samtools view -b -F 4 $DATA_DIR/aln/$readid.bam > $DATA_DIR/aln/$readid.filtered.bam
			echo -e $sep
		else
			echo "Could not find all files"
		fi
	fi
done
