#!/usr/bin/env python

# Author: Joel Gruselius 2019
# Color balance checker for index sequences in Illumina sequencing
# Given a list of strings of nucleotide sequences, check if both color
# channels (red, green) are represented.

import argparse
import re

# MAYBE: Ensure equal length
# MAYBE: Make sure no index starts width GG
# TODO: Print aligned sequences indicating (w color?) unbalanced positions
#
# NovaSeq (2-channel) color chemistry:
# Base Red  Green Result
# A    1    1     Clusters that show intensity in both the red and green channels.
# C    1    0     Clusters that show intensity in the red channel only.
# G    0    0     Clusters that show no intensity at a known cluster location.
# T    0    1     Clusters that show intensity in the green channel only.

test_seqs = ['ATCTGTAG', 'GTCCAAGT', 'TTGGAACC', 'AGTTCAGT']

many_seqs = [
    "GGTTTACT",
    "GTAATCTT",
    "CCACTTAT",
    "CACTCGGA",
    "TGGTAAAC",
    "GTTGCAGC",
    "ATGAATCT",
    "GTATGTCA",
    "TTTCATGA",
    "TACTCTTC",
    "CCTAGACC",
    "TAACAAGG",
    "GTGGTACC",
    "TTTACATG",
    "TGATTCTA",
    "TAATGACC",
    "CAGTACTG",
    "GTGTATTA",
    "TCAGCCGT",
    "ACATTACT",
    "AGGTATTG",
    "TTCAGGTG",
    "CCTCATTC",
    "CCAAGATG",
    "TATGATTC",
    "ACTTCATA",
    "ACAATTCA",
    "CCCTAACA",
    "TTCGCCCT",
    "CCCAATAG",
    "GCGATGTG",
    "GCCATTCC",
    "CTAGGTGA",
    "AATAATGG",
    "CGACTTGA",
    "CTCGTCAC",
    "CATTAGCG",
    "GACTACGT",
    "GAGCAAGA",
    "CCACTACA",
    "CGCTATGT",
    "CGTTAATC",
    "ATTACTTC",
    "CATGCGAT",
    "CTGCGGCT",
    "CGGAGCAC",
    "CTGACGCG",
    "TAGGATAA",
    "ACAGAGGT",
    "AAACCTCA",
    "GTCTCTCG",
    "ATTTGCTA",
    "CACGCCTT",
    "CGTGCAGA",
    "GGTATGCA",
    "AGCTATCA",
    "GCATCTCC",
    "AAAGTGCT",
    "GTTGAGAA",
    "GCAACAAA",
    "ATAGTTAC",
    "CATGAACA",
    "TATGAGCT",
    "TTGTTGAT",
    "TCTTAAAG",
    "CTGTAACT",
    "GCGCAGAA",
    "AGGAGATG",
    "TTGTTTCC",
    "CAAGCTCC",
    "TAGGACGT",
    "ACACTGTT",
    "GAAACCCT",
    "ACCGTATG",
    "TCTCAGTG",
    "CAATACCC",
    "AAATGTGC",
    "GCTTGGCT",
    "TCGCCAGC",
    "GTAATTGC",
    "GTCCGGTC",
    "GTTCCTCA",
    "GAGGATCT",
    "CTTTGCGG",
    "AAGCGCTG",
    "GCGAGAGT",
    "TTATCGTT",
    "GGCGAGTA",
    "AGTGGAAC",
    "TACCACCA",
    "TCTCGTTT",
    "GCACAATG",
    "ACCGGCTC",
    "TGATGCAT",
    "ATTCTAAG",
    "GACAGCAT"
]

# Verify that all strings only consist of AGTC
# and strip leading/trailing whitespace:
def validate(seqs):
    p = re.compile(r"[^AGTC]")
    for seq in seqs:
        s = seq.strip().upper()
        if p.search(s):
            raise ValueError("{} contains unexpected symbols".format(seq))
        yield s

# One approach is to convert each base into color channel representation

# Generates a tuple indicating color channel (red,green) for every nt in seq
def base_to_col_chan(seq):
    conv = {
        "A": (1, 1),
        "T": (0, 1),
        "G": (0, 0),
        "C": (1, 0)
    }
    for nt in seq:
        yield conv[nt]

# Use the above for multiple sequences
def seqs_to_col_chan(seqs):
    for seq in seqs:
        yield list(base_to_col_chan(seq))

# Use list comprehension to translate a list of sequences (strings) to
# list of list of color channel tuples:
def conv_to_col_chan(seqs):
    # Map to translate base to color channel tuple (red, green):
    conv = { 
        "A": (1, 1),
        "T": (0, 1),
        "G": (0, 0),
        "C": (1, 0)
    }
    return [[conv[nt] for nt in seq] for seq in seqs]

# Sum that short version
# (takes list of color channel tuples)
# (cannot deal w seqs of different length)
# Make a list of channel counts by index:
def sum_chan_short(chan_seqs):
    return [list(map(sum, zip(*e))) for e in zip(*chan_seqs)]

# Sum that longer version
# (taskes list of color channel tuples)
# (can deal with seqs of dif length)
def sum_chan(chan_seqs):
    counter = []  # Where length is equal to the longest seq in seqs
    for seq in chan_seqs:
        for i, chan in enumerate(seq):
            if i == len(counter):
                counter.append([0, 0])
            counter[i][0] += chan[0]
            counter[i][1] += chan[1]
    return counter

# Check for any zeroes in the summed-color-channel-by-position list
def check_balance(chan_sums):
    return [all(counts) for counts in chan_sums]

# An alternative approach is to count how many times each base occurs in each
# position

# Returns a list of base counters, where each position in the seq has a dict
# with counts of each of the four nucleotides occurring in this position.
def count_base_by_pos(seqs):
    c = []
    for seq in seqs:
        for i, nt in enumerate(seq):
            if i >= len(c):
                c.append({"A": 0, "C": 0, "T": 0, "G": 0})
            c[i][nt] += 1
    return c

# Takes a list of base counters and checks if bases in both colors channels
# occur for every position.
def is_balanced(base_counter):
    return [(p["A"] + p["C"]) * (p["A"] + p["T"]) > 0 for p in base_counter]

# Put it in words:
def summarize(balance_list):
    for i, pos in enumerate(balance_list):
        if not pos:
            print("There is not balance in position {:d}".format(i+1))
    if all(balance_list):
        print("All positions are balanced!")

def pretty_print(seqs):
    color = {
        "red": " \033[01;31m{0}\033[00m",
        "green": " \033[1;32m{0}\033[00m",
        "cyan": " \033[1;36m{0}\033[00m",
        "none": " {0}"
    }
    col_chan = {
        "A": "cyan",
        "T": "green",
        "G": "none",
        "C": "red"
    }

    for seq in seqs:
        for x in seq:
            print(color[col_chan[x]], end="")
        print("")

# OO approach:

class ColorBalanceChecker:
    # Map to translate base to color channel tuple (red, green):
    conv = { 
        "A": (1, 1),
        "T": (0, 1),
        "G": (0, 0),
        "C": (1, 0)
    }
    # Alt. map to translate base to color channel tuple (red, green):
    cinv = {
        'A': {'green': 1, 'red': 1},
        'T': {'green': 0, 'red': 1},
        'G': {'green': 0, 'red': 0},
        'C': {'green': 1, 'red': 0}
    }

    def __init__(self, seqs):
        self.validate(seqs).count_base_by_pos().check_balance_general()
        # self.validate(seqs).conv_to_col_chan().sum_chan()

    # Verify that all strings only consist of AGTC, sotre unique lenghts and
    # strip leading/trailing whitespace:
    def validate(self, seqs):
        valid = []
        lengths = set()
        p = re.compile(r"[^AGTC]")
        for seq in seqs:
            s = seq.strip().upper()
            if p.search(s):
                raise ValueError("{} contains unexpected symbols".format(seq))
            valid.append(s)
            lengths.add(len(s))
        self.seqs = valid
        self.lengths = lengths
        return self

    # Returns a list of base counters, where each position in the seq has a dict
    # with counts of each of the four nucleotides occurring in this position.
    def count_base_by_pos(self):
        c = []
        for seq in self.seqs:
            for i, nt in enumerate(seq):
                if i >= len(c):
                    c.append({"A": 0, "C": 0, "T": 0, "G": 0})
                c[i][nt] += 1
        self.base_counts = c
        return self

    def check_balance(self):
        self.balance = [(p["A"] + p["C"]) * (p["A"] + p["T"]) > 0 for p in self.base_counter]
        return self

    # This summariser takes a dict to make it more general
    def check_balance_general(self):
        b = []
        for pos in self.base_counts:
            green = 0
            red = 0
            for nt, chans in self.cinv.items():
                green += pos[nt] * chans['green']
                red += pos[nt] * chans['red']
            b.append(green > 0 and red > 0)
        self.balance = b
        return self

    def conv_to_col_chan(self):
        self.chans = [[self.conv[nt] for nt in seq] for seq in self.seqs]
        return self

    # Sum those tuples (can deal with seqs of dif length)
    def sum_chan(self):
        c = []
        if len(self.lengths) == 1:
            c = [list(map(sum, zip(*e))) for e in zip(*self.chans)]
        else:
            for seq in self.chans:
                for i, chan in enumerate(seq):
                    if i == len(c):
                        c.append([0, 0])
                    c[i][0] += chan[0]
                    c[i][1] += chan[1]
        self.counter = c
        return self

    # Check for any zeroes in the summed-color-channel-by-position list
    def check_balance(self):
        self.balance = [all(counts) for counts in self.counter]
        return self

    # Put it in words:
    def summarize(self):
        for i, pos in enumerate(self.balance):
            if not pos:
                print("There is not balance in position {:d}".format(i+1))
        if all(self.balance):
            print("All positions are balanced!")

    # Print all sequences indicating channel by letter color and mark
    # unbalanced positions:
    def pretty_print(self):
        colorize = {
            "red": " \033[0;31m{0}\033[00m",
            "green": " \033[0;32m{0}\033[00m",
            "cyan": " \033[0;36m{0}\033[00m",
            "none": " {0}"
        }
        col_chan = {
            "A": "cyan",
            "T": "green",
            "G": "none",
            "C": "red"
        }
        for i in range(max(self.lengths)):
            print(" {:d}".format(i+1), end="")
        print("")
        for seq in self.seqs:
            for x in seq:
                print(colorize[col_chan[x]].format(x), end="")
            print("")
        for pos in self.balance:
            if not pos:
                print(" ↑", end="")
            else:
                print("  ", end="")
        print("")
        return self

def main(args):
    # Version 1:
    # summarize(check_balance(sum_chan(seqs_to_col_chan(validate(args.seqs)))))
    # and so on...
    # I like this version better:
    cbc = ColorBalanceChecker(args.seqs)
    cbc.pretty_print()
    cbc.summarize()

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Check if a collection of index "
        "sequences are color balanced")
    p.add_argument("seqs", nargs="+", help="Nucleotide sequences (can be "
        "different length)")
    main(p.parse_args())
