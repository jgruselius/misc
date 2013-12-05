# Print header row:
firstfile=$(ls -d data/*/*/*hs_metrics | head -1)
header=$(cat $firstfile | head -q -n 7 | tail -n 1 | tr "\t" ",")
echo -e "SAMPLE_ID,PROJECT,"$header

# For each sample:
for folder in $(echo data/*/)
do
  	# If the sample has been run on more than 1 FC:
        if [ -d $folder"TOTAL" ]; then
                spath=$folder"TOTAL"
        else
            	spath=$folder"*/"
        fi
	for file in $(find $spath -mindepth 1 -maxdepth 1 -name *.hs_metrics);
        do
          	project=$(basename $PWD)
                sample=$(basename $folder)
                metrics=$(cat $file | head -q -n 8 | tail -n 1 | tr "," "." | tr "\t" $
                echo -e $sample","$project","$metrics
        done
done
