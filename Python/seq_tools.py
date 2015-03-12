# Author: Joel Gruselius
# Version: 2013-11-21
# Description: Various simple but useful methods for nucleotide sequences
# to be used in a terminal.

import argparse
import time

COMPL_MAP = {'A':'T','T':'A','C':'G','G':'C'}

CODON_MAP = {
	'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
	'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
	'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
	'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
	'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
	'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
	'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
	'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
	'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
	'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
	'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
	'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
	'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
	'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
	'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
	'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
	}

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
	return text.format(n, *(list(bases) + [100*c/n for c in counts]))

def find_kmers(seq, k):
	kmers = []
	n = len(seq)
	for i in range(0, n-k+1):
		kmers.append(seq[i:i+k])
	return kmers

def count_kmers(seq, k):
	kmers = find_kmers(seq, k)
	counts = {}
	for k in kmers:
		counts[k] = seq.count(k)
	return counts

def translate(seq):
	codons = (seq[i:i+3] for i in range(0,len(seq),3))
	peptide = (CODON_MAP[c] if c in CODON_MAP else "?" for c in codons)
	return "".join(peptide)

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
		"i":stats, "info":stats,
		"t":translate, "translate":translate,
		"k":find_kmers, "find_kmers":find_kmers,
		"kc":count_kmers, "count_kmers":count_kmers
	}
	if args.command in options:
		if args.command == "s":
			print(options[args.command](args.seq, args.query))
		elif args.command == "k" or args.command == "kc":
			print(options[args.command](args.seq, int(args.k)))
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
	s.add_parser("t", help="Return the translated sequence").add_argument("seq", help=helpString)
	sp = s.add_parser("k", help="Find k-mers")
	sp.add_argument("seq", help=helpString)
	sp.add_argument("k", help="k-mer length")
	sp = s.add_parser("kc", help="Count k-mers")
	sp.add_argument("seq", help=helpString)
	sp.add_argument("k", help="k-mer length")
	args = p.parse_args()
	main(args)

# Other things to implement:
# -Barcode dictionary: Enter barcode sequence and return index ID
