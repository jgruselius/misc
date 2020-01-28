#!/usr/bin/env python3

# Author: Joel Gruselius, Jan 2020
# Script for checking index clashes
# Input one or several nucleotide sequences and print any matches found in
# the index reference database.
# Usage:
#   index_finder --ref <reference_list> <index_seq>...

import sys
import argparse
import re
import os
import errno
import sqlite3

COMPL_MAP = {"A": "T", "T": "A", "C": "G", "G": "C"}

def rev(seq):
    return seq[::-1]

def compl(seq):
    c = [COMPL_MAP[nt] for nt in seq]
    return "".join(c)

def rev_compl(seq):
    rc = [COMPL_MAP[nt] for nt in seq[::-1]]
    return "".join(rc)

# Make sure the string to search only contains allowed characters
# (and not something like ";delete table"). Drop those that don't pass:
def filter_good_seqs(seqs):
    passed = []
    pattern = re.compile("^[ATCGN]+$")
    for seq in seqs:
        s = seq.strip().upper()
        if pattern.search(s):
            # Allow N's by replacing to _ (sql syntax):
            s = s.replace("N", "_")
            passed.append(s)
        else:
            print('ERROR: String "{}" contains invalid characters, omitting...'
                  .format(seq), file=sys.stderr)
    return passed

def something(seqs):
    path = "/Users/joelgruselius/tmp/index.db"
    TABLE = "indexes"
    COLUMN = "i7 sequence"
    HEADER = ("Name", "Sequence", "i7", "i5", "Vendor", "Kit" , "LIMS category", "Status")
    # Filter for proper sequences:
    passed = filter_good_seqs(seqs)
    # If no sequences are left - exit.
    if not len(passed):
        print('No valid sequences given, exiting...')
        sys.exit(0)
    try:
        db = sqlite3.connect(path)
        c = db.cursor()
        query_str = 'SELECT * FROM "{}" WHERE "{}" LIKE'.format(TABLE, COLUMN)
        for seq in passed:
            print("{} matches".format(seq))
            query = '{} "{}%"'.format(query_str, seq)
            c.execute(query)
            # Print
            if c.fetchone():
                print("\t{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}"
                          .format("Name", "i7", "i5", "Kit", "Vendor", "Status"))
                for row in c:
                    print("\t{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}"
                          .format(row[0], row[2], row[3], row[4], row[5], row[6]))
            else:
                print("\tNo matches")
    except:
        raise
        #print(e, file=sys.stderr)
    finally:
        db.close()

def main(args):
    # Check if database exists:
    if not os.path.isfile(args.ref):
        # File not found
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), args.ref)
    # 
    if args.list:
        # One could output some database stats:
        print("\nTotal barcodes parsed in reference dict: {}".format(n))
        print("Unique barcodes in reference dict: {}".format(len(ref_dict)))
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
    p.add_argument("--ref", required=True, help="Reference database containing"
            " known index sequences")
    p.add_argument("--length", type=int, choices=range(4,8), help="Set the "
            "number of letters to consider query strings")
    main(p.parse_args())
