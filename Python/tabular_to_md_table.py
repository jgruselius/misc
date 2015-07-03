# Python script for coverting tab-separated data to Markdown tables

import sys
import fileinput
import re

def _convert_lines():
	for i, line in enumerate(fileinput.input()):
		conv = _convert(line)
		print(conv)
		if i == 0:
			cols = len(line.strip().split("\t"))
			print("|{}".format(cols*("----|")))

def _convert(text):
	return "| {} |".format(re.sub("\t"," | ",text.strip()))

def main():
	_convert_lines()

if __name__ == "__main__":
	main()
