import sys
import json
import csv
import re

def parse(in_file, out_file):
	# Data object is of format:
	# 	Total flowcells:    data["total_rows"]
	# 	Offset:             data["offset"]
	# 	Flowcell data:      data["rows"]
	# Where data["rows"] is a list and if fc = data["rows"][n]:
	# 	Database hash key:  fc["id"]
	#	Flowcell/run ID:    fc["key"]
	#	Lane data:          fc["value"]
	# Where fc["value"] is a list and if n is the lane index then fc["value"][n-1]
	# is of format {barcode_sequence : million_reads}

	data = json.load(in_file)

	# Write comma-separated output with format RUN_ID,LANE,BARCODE,READS:
	writer = csv.writer(out_file, delimiter=",")
	writer.writerow(["RUN_ID","LANE","BARCODE","READS"])

	# As an inappropriately long comprenhension:
	writer.writerows([[fc["key"], i+1, bc, reads] \
		for fc in data["rows"] \
		for i, lane in enumerate(fc["value"]) \
		for bc, reads in lane.items()]
	)

def parse_big(in_file, out_file):
	# Write comma-separated output with format RUN_ID,LANE,BARCODE,READS:
	writer = csv.writer(out_file, delimiter=",")
	writer.writerow(["RUN_ID","LANE","BARCODE","READS"])

	for line in in_file:
		if re.match("\{\"id", line):
			fc = json.loads(line.rstrip("\r\n,"))
			writer.writerows([[fc["key"], i+1, bc, reads] \
				for i, lane in enumerate(fc["value"]) \
				for bc, reads in lane.items()]
			)

if __name__ == "__main__":
	parse_big(sys.stdin, sys.stdout)
