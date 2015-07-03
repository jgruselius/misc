#!/bin/bash

# Print header row:
firstfile=$(find . -name "*.hs_metrics" | head -1)
header=$(head -q -n 7 "$firstfile" | tail -n 1 | tr "\t" ",")
echo -e "SAMPLE_ID,PROJECT,""$header"

if [ -d "data/" ]; then
		spath="data/*/"
	else
		spath="./*/"
	fi

# Fix:
spath="./*/"

# For each sample:
for folder in $(echo "$spath")
do
	# If the sample has been run on more than 1 FC:
	if [ -d "$folder""TOTAL" ]; then
		spath=$folder"TOTAL"
	else
		spath=$folder"*/"
	fi
	for file in "$spath""*.hs_metrics";
	do
		project=$(basename "$PWD")
		sample=$(basename "$folder")
		metrics=$(head -q -n 8 "$file" | tail -n 1 | tr "," "." | tr "\t" ",")
		echo -e "$sample,$project,$metrics"
	done
done
