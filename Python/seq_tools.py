# Author: Joel Gruselius
# Version: 2013-11-21
# Description: Various simple but useful methods for nucleotide sequences
# to be used in a terminal.

import argparse
import time

COMPL_MAP = {'A':'T','T':'A','C':'G','G':'C'}

def length(seq):
	return len(seq)

def reverse(seq):
	return seq[::-1]

def complement(seq):
	compl = [COMPL_MAP[nt] for nt in seq]
	return "".join(compl)

def reverseComplement(seq):
	revCompl = [COMPL_MAP[nt] for nt in seq[::-1]]
	return "".join(revCompl)

def search(seq, query):
	seqList = [substr.lower() for substr in seq.split(query)]
	match = "|{0}|".format(query)
	return match.join(seqList)

def stats(seq):
	seq = seq.replace(" ","")
	n = len(seq)
	bases = COMPL_MAP.keys()
	counts = (seq.count(base) for base in bases)
	text = "Length: {0}, {1}: {5}%, {2}: {6}%, {3}: {7}%, {4}: {8}%"
	return text.format(n, *(bases + [100*c/n for c in counts]))

def lookup(seq):
	pass

def help():
	return "Usage:\n\tpython <command> <sequence>\n"

def main(args):
	t = time.clock()
	options = {"l":length, "length":length, 
		"r":reverse, "reverse":reverse,
		"c":complement, "complement":complement,
		"rc":reverseComplement, "rcomplement":reverseComplement,
		"s":search, "search":search,
		"i":stats, "info":stats
	}
	if args.command in options:
		if args.command == "s":
			print(options[args.command](args.seq, args.query))
		else:
			print(options[args.command](args.seq))
	else:
		print(help())
	print("Timer: {0} s".format(time.clock()-t))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="Various simple but useful " +
		"methods for nucleotide sequences.")
	s = p.add_subparsers(help="Commands",dest="command")
	helpString = "Nucleotide sequence"
	s.add_parser("r", help="Return the reverse sequence").add_argument("seq", help=helpString)
	s.add_parser("c", help="Return the complement sequence").add_argument("seq", help=helpString)
	s.add_parser("rc", help="Return the reverse-complement sequence").add_argument("seq", help=helpString)
	sp = s.add_parser("s", help="Search the sequence")
	sp.add_argument("seq", help=helpString)
	sp.add_argument("query", help="The " + helpString + " to search for")
	s.add_parser("i", help="Show info about sequence").add_argument("seq", help=helpString)
	args = p.parse_args()
	main(args)

# Other things to implement:
# -Barcode dictionary: Enter barcode sequence and return index ID
