# Python script for coverting tab-separated data to Markdown tables

import sys
import fileinput
import re
import itertools

# Maximum width to pad columns:
COL_MAX = 25

# Simple non-aligned version:
def _convert_lines():
	for i, line in enumerate(fileinput.input()):
		conv = _convert(line)
		print(conv)
		# Add dashes efter header row:
		if i == 0:
			cols = len(line.strip().split("\t"))
			print("|{}".format(cols*("----|")))

# Replace tabs with horizontal lines:
def _convert(text):
	return "| {} |".format(re.sub("\t"," | ",text.strip()))

# Checks whether the provided value can be converted to a float:
def _is_number(x):
	try:
		float(x)
		return True
	except:
		return False

# This version pads columns with whitespace according to the widest one and
# aligns numeric columns to the right:
def _convert_lines2():
	# Split input into 2D list on tab character:
	table = [line.strip().split("\t") for line in fileinput.input() if line.strip()]
	# Transpose:
	table_t = list(map(list, itertools.zip_longest(*table)))
	# Check whether all values in column except heading is numeric (or blank):
	numeric = [all([not (x and x.strip()) or _is_number(x) for x in row[1:]]) for row in table_t]
	# Determine the widest string in column:
	lengths = [[len(x) if x else 0 for x in row] for row in table_t]
	lengths = [max(x) if max(x) <= COL_MAX else COL_MAX for x in lengths]
	for i, line in enumerate(table):
		text = []
		for j, col in enumerate(line):
			if numeric[j]:
				text.append(col.rjust(lengths[j]))
			else:
				text.append(col.ljust(lengths[j]))
		print("| {} |".format(" | ".join(text)))
		# Add row with dashes after header:
		if i == 0:
			print("|-{}-|".format("-|-".join(["-".ljust(lengths[n],"-") for n in range(len(line))])))

def main():
	_convert_lines2()

if __name__ == "__main__":
	main()
