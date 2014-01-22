import json
import csv

file="index-lane-yields.json"
out_file="out.csv"

with open(file) as raw_data:
	data = json.load(raw_data)

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

# Reformat to RUN-ID,LANE,BARCODE,YIELD
formd = []
for fc in data["rows"]:
	fc_id = fc["key"]
	for lane_index, lane in enumerate(fc["value"]):
		formd.append([[fc_id, lane_index, bc, m_reads] for bc, m_reads in lane.iteritems()])

with open(out_file, "wb") as csv_file:
	writer = csv.writer(csv_file, delimiter=",")
	writer.writerow(["RUN-ID","LANE","BARCODE","M_READS"])
	for rows in formd:
		writer.writerows(rows)
