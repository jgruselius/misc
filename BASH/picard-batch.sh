#!/bin/bash -l

#SBATCH -A b2013064
#SBATCH -p node
#SBATCH -n 1
#SBATCH -e picard-batch-%j.err
#SBATCH -o picard-batch-%j.out
#SBATCH --mail-user joel.gruselius@scilifelab.se
#SBATCH --mail-type=ALL

module load bioinfo-tools
module load picard

DATA_DIR=/proj/b2013064/nobackup/joel
REF=/bubo/nobackup/uppnex/reference/biodata/genomes/Hsapiens/hg19/seq/hg19.fa
TARGET_REF=$DATA_DIR/ref/NexteraRapidCapture.targets.wheader.txt
BAIT_REF=$DATA_DIR/ref/NexteraRapidCapture.baits.wheader.txt
OUT=$DATA_DIR/stat

# Print all file paths for informations sake:
sep="\n"
echo -e "REFERENCE:$REF"
echo -e "TARGET REGIONS:\n$TARGET_BED"
echo -e "OUTPUT DIR:\n$DATA_DIR/stat/\n$DATA_DIR/aln/"
echo "FILES:"
for file in "$@";do echo "$(basename $file)";done
echo -e $sep

files="$@"
for file in ${files[@]}; do
	input=$(readlink -e $file)
	readid=$(basename ${file%.bam})
	
	# Calculate insert size metrics:
	time java -Xmx16g -jar $PICARD_HOME/CollectInsertSizeMetrics.jar MINIMUM_PCT=0 \
			HISTOGRAM_FILE=$OUT/$readid.pdf \
			INPUT=$input \
			OUTPUT=$OUT/$readid.size-metrics.tsv \
			HISTOGRAM_WIDTH=600
	
	# Flag reads identified as duplicates:
	time java -Xmx16g -jar $PICARD_HOME/MarkDuplicates.jar INPUT=$input \
			OUTPUT=$DATA_DIR/aln/$readid.marked.bam \
			METRICS_FILE=$OUT/$readid.duplicate-metrics.tsv \
			ASSUME_SORTED=true
	
	# Calculate target enrichment metrics:
	time java -Xmx16g -jar $PICARD_HOME/CalculateHsMetrics.jar \
			TARGET_INTERVALS=$TARGET_REF \
			BAIT_INTERVALS=$BAIT_REF \
			INPUT=$input OUTPUT=$OUT/$readid.target-metrics.tsv \
			REFERENCE_SEQUENCE=$REF
done
