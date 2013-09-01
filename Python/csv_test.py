#! /usr/bin/env python

import sys
import csv

def main(args):
	# Read data from file:
	inFile = open(args[0], "rb")
	inData = inFile.read()

	# Check format:
	dialect = csv.Sniffer().sniff(inData)
	lt = repr(dialect.lineterminator)

	print("\nHas header: %s\nDelimiter: \'%s\'\nLine terminator: %s\n" %
	(csv.Sniffer().has_header(inData), dialect.delimiter, lt))

if __name__ == "__main__":
	main(sys.argv[1:])