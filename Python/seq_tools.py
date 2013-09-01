# Author: Joel Gruselius
# Version: 2012-12-21
# Description: Various simple but useful methods for nucleotide sequences
# to be used in a terminal.

import argparse
import time

def length(seq):
	return len(seq)

def reverse(seq):
	return seq[::-1]

def complement(seq):
	complementMap = {'A':'T','T':'A','C':'G','G':'C'}
	compl = [complementMap[nt] for nt in seq]
	return "".join(compl)

def reverseComplement(seq):
	complementMap = {'A':'T','T':'A','C':'G','G':'C'}
	revCompl = [complementMap[nt] for nt in seq[::-1]]
	return "".join(revCompl)

def search(seq, query):
	seqList = [substr.lower() for substr in seq.split(query)]
	match = "|{0}|".format(query)
	return match.join(seqList)

def stats(seq):
	n = len(seq)
	counts = seq.count("A"), seq.count("T"), seq.count("C"), seq.count("G")
	return "Length: {0}, A: {1}%, T: {2}%, C: {3}%, G: {4}%".format(n,
		*[100*c/n for c in counts])

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
	if args.mode in options:
		print(options[args.mode](args.seq))
	else:
		print(help())
	print("Timer: {0} s".format(time.clock()-t))

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="Various simple but useful " +
		"methods for nucleotide sequences.")
	p.add_argument("mode", metavar="<mode>", help="The transformation to apply",
		choices=("l","r","c","rc","s","i"))
	p.add_argument("seq", metavar="<seq>", help="Nucleotide sequence")
	s = p.add_subparsers(help="subparser help").add_parser("s", help="query help")
	s.add_argument("query", metavar="[query]", help="Query sequence for mode 's'")
	args = p.parse_args()
	main(args)

# Other things to implement:
# -Barcode dictionary: Enter barcode sequence and return index ID
