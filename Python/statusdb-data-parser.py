import sys
import json
import csv
import time

def parse(in_file, out_file):
	# Data object is of format:
	# 	Total flowcells:	data["total_rows"]
	# 	Offset: 			data["offset"]
	# 	Flowcell data:		data["rows"]
	# Where data["rows"] is a list and if fc = data["rows"][n]:
	# 	Database hash key:	fc["id"]
	#	Flowcell/run ID:	fc["key"]
	#	Lane data:			fc["value"]
	# Where fc["value"] is a list and if n is the lane index then fc["value"][n-1]
	# is of format {barcode_sequence : million_reads}

	data = json.load(in_file)

	# Reformat to RUN-ID,LANE,BARCODE,YIELD

	# Write comma-separated output:
	writer = csv.writer(out_file, delimiter=",")

	# As an inappropriately long comprenhension:
	writer.writerows([[fc["key"], i+1, bc, reads] \
		for fc in data["rows"] \
		for i, lane in enumerate(fc["value"]) \
		for bc, reads in lane.iteritems()]
	)

	# As a nested loop:
	# for fc in data["rows"]:
	# 	for i, lane in enumerate(fc["value"]):
	# 		for bc, reads in lane.iteritems():
	# 			writer.writerow([fc["key"], i+1, bc, reads])

if __name__ == "__main__":
	t1 = time.clock()
	parse(sys.stdin, sys.stdout)
	print(time.clock() - t1)
	
