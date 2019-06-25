#!/usr/bin/env python

# Author: Joel Gruselius, Dec 2018 
# Script for checking index clashes
# Input one or several nucleotide sequences and print any matches found in
# the index reference file. This version is only good for checking for
# full matches.
# It is pretty useful though to list overlapping indexes in the reference file.
# Usage:
#   index_finder --ref <reference_list> <index_seq>...

# TODO: Show sequences matching the first six bases not just complete matches
# TODO: Specify cache dir

import argparse
import re
import hashlib
import json
import os
import errno

COMPL_MAP = {"A": "T", "T": "A", "C": "G", "G": "C"}

def file_hash(path):
    BUF_SIZE = 65536
    md5_hash = hashlib.md5()
    with open(path, "rb") as f:
        data = f.read(BUF_SIZE)
        while data:
            md5_hash.update(data)
            data = f.read(BUF_SIZE)
    return md5_hash.hexdigest()

def rev(seq):
    return seq[::-1]

def compl(seq):
    c = [COMPL_MAP[nt] for nt in seq]
    return "".join(c)

def rev_compl(seq):
    rc = [COMPL_MAP[nt] for nt in seq[::-1]]
    return "".join(rc)

# Build a dict of know index sequences from a text file:
def build_index_dict(path, length):
    ref_dict = {}
    if length is None:
        seq_pattern = re.compile(r"(?<![ATCG])[ATCGN]{4,}")
    else:    
        seq_pattern = re.compile(r"(?<![ATCG])[ATCGN]{{{}}}".format(length))
    with open(path, "r") as ref:
        for line in ref:
            match = set(seq_pattern.findall(line))
            if match:
                for m in match:
                    ref_dict.setdefault(m, []).append(line.strip())
    return ref_dict

def load_index_dict(path):
    with open(path, "r") as f:
        d = json.load(f)
    return d

def save_index_dict(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f)

def print_index_dict(ref_dict):
    for seq, matches in ref_dict.items():
        if len(matches) > 1:
            print(seq)
            for match in matches:
                print("\t{}".format(match))

def main(args):
    if not os.path.isfile(args.ref):
        # File not found
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), args.ref)
    md5 = file_hash(args.ref)
    cache = "{}{}.json".format(md5, args.length or "")
    if not args.rebuild and os.path.isfile(cache):
        print("Loading cached index dict ({})".format(cache))
        ref_dict = load_index_dict(cache)
    else:
        ref_dict = build_index_dict(args.ref, args.length)
        print("Caching index dict ({})".format(cache))
        save_index_dict(ref_dict, cache)
    if args.list:
        print_index_dict(ref_dict)
    else:
        for arg in args.seqs:
            if args.length:
                seq = arg[:args.length]
            else:
                seq = arg
            if seq in ref_dict:
                matches = ref_dict[seq]
                print("{} found in:".format(seq))
                for m in matches:
                    print("\t{}".format(m))
            else:
                print("{}: No matches found".format(seq))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Find index clashes")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--seqs", nargs="+", help="All sequences to search for")
    g.add_argument("--list", action="store_true", default=False,
            help="Print non-unique indexes in the reference list")
    p.add_argument("--ref", required=True, help="Reference text file containing"
            " known index sequences")
    p.add_argument("--rebuild", action="store_true", help="Don't use any cached"
            " reference object")
    p.add_argument("--length", type=int, choices=range(4,8), help="Set the "
            "number of letters to consider, both in the query strings and "
            "when building the reference")
    main(p.parse_args())
