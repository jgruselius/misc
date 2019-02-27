# #!/usr/bin/env python

# Author: Joel Gruselius, Dec 2018 
# Script for checking index clashes
# Input one or several nucleotide sequences and print any matches found in
# the an index reference file using grep.
# Usage:
#   index_finder --ref <reference_list> <index_seq>...

import argparse
import os
import errno
import subprocess

def main(args):
    if not os.path.isfile(args.ref):
        # File not found
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), args.ref)

    # Build pattern from args:
    pattern = "|".join(args.seqs)
    pattern = "(?<![ATCG])({})".format(pattern)
    # Construct grep command:
    command = ["ggrep", "-C", "0", "--no-group-separator", "--color=always", "-P", "-e", pattern, args.ref]
    # grep gives a non-zero exit code on no match
    out = subprocess.check_output(command)
    print(out.decode("ascii"))

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Find index clashes")
    p.add_argument("seqs", nargs="+", help="All sequences to search for")
    p.add_argument("--ref", required=True, help="Reference text file containing known index sequences")
    main(p.parse_args())
