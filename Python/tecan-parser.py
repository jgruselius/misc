#!/usr/bin/env python

import sys
import re
import fileinput
import csv
import os

def parse(iterable):
	# Pattern for matching "Layout" ID:
	p = re.compile(r"(S[MT])1_(\d{1,2})")
	# Read in the csv file:
	for line in iterable:
		# Clean the string:
		vals = line.strip(" ,\r\n").replace("#","").replace(" ","").split(",")
		# Move the marked value to a separate column:
		if "#" in line:
			vals.append("#")
		else:
			vals.append("")
		# Filter out all rows with sample and standard entries and
		# only use the "1/3" replicate:
		m = p.match(vals[1])
		if m and vals[2] == "1/3":
			# Substitute replicate with index:
			vals[2] = m.group(2)
			# Assign a type and source well:
			if m.group(1) == "SM":
				vals[1] = "Sample"
				vals[0] = index_to_well(m.group(2))
			else:
				vals[1] = "Standard"
				vals[0] = ""
			# Skip some columns:
			yield(list(vals[i] for i in (0,1,2,4,5,7,8,9)))

def convert(file_in, file_out):
	# Make a list of it to be able to sort:
	data = list(parse(file_in))
	# Sort the results on type then index:
	data.sort(key=lambda x: (x[1], int(x[2])))
	# Create the header:
	header = [
		"Well",
		"Type",
		"Index",
		"Raw mean",
		"Raw standard dev",
		"Conc mean (ng/uL)",
		"Conc CV",
		"Mark"
	]
	# Write data:
	writer = csv.writer(file_out)
	writer.writerow(header)
	writer.writerows(data)

# Convert an index to a plate coordinate, e.g. 8 => H1
def index_to_well(index):
	i = int(index)
	row = chr(64 + ((i-1) % 8 + 1))
	col = int(((i-1) - (i-1) % 8) / 8 + 1)
	return "{}{}".format(row, col)

def main(args):
	if args and not args[0] == "-" and not all(os.path.isfile(p) for p in args):
			print("Usage:\n\t{} <file> [files ...]\nAlso accepts stdin".format(sys.argv[0]))
	else:
		convert(fileinput.input(), sys.stdout)

if __name__ == "__main__":
	main(sys.argv[1:])
