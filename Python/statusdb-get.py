import sys
import json
import csv
import re
import requests
import getpass
import argparse

def get_data(url, js_path):
	user = input("User name for {0}:".format(url))
	passw = getpass.getpass("Password:")

	with open(js_path) as js_file:
		js = js_file.read()

	### Format JavaScript ###
	# Replace newlines and remove tabs:
	js = js.replace("\n", " ")
	js = js.replace("\t", "")
	# Remove JS comments:
	js = re.sub("(\/\*)[^\*]+\*\/", "", js).strip()

	### Request data with POST ###
	post_data = json.dumps({"map": js})
	header={"content-type": "application/json"}
	response = requests.post(url, headers=header, auth=(user, passw), data=post_data, stream=True)
	
	return response

def write_json(resp, out_file):
	for line in resp.iter_lines(decode_unicode=True):
		out_file.write(line)

def write_csv(resp, out_file):
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

	# Write comma-separated output with format RUN_ID,LANE,BARCODE,READS:
	writer = csv.writer(out_file, delimiter=",")
	writer.writerow(["RUN_ID","LANE","BARCODE","READS"])

	for line in resp.iter_lines(decode_unicode=True):
		if re.match("\{\"id", line):
			fc = json.loads(line.rstrip("\r\n,"))
			writer.writerows([[fc["key"], i, bc, reads] \
				for i, lane in fc["value"].items() \
				for bc, reads in lane.items()]
			)

if __name__ == "__main__":
	# Parse command-line arguments:
	parser = argparse.ArgumentParser(description="Query a CouchDB database")
	parser.add_argument("jsfile", help="File containing JavaScript map function")
	parser.add_argument("--out", help="File to write response to")
	parser.add_argument("--url", help="Database URL", default="http://tools-dev.scilifelab.se:5984/flowcells/_temp_view")
	parser.add_argument("--csv", help="Convert response to CSV", action="store_true")
	args = parser.parse_args()
	
	if args.csv:
		write_func = write_csv
	else:
		write_func = write_json

	resp = get_data(args.url, args.jsfile)

	if args.out:
		with open(args.out, "w") as out_file:
			write_func(resp, out_file)
	else:
		write_func(resp, sys.stdout)


