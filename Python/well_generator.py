#! /usr/bin/env python3

import argparse
import string

def main(args):
    rows = string.ascii_uppercase[:8]
    cols = range(1, 13)
    if args.r:
        wells = [(r, c) for r in rows for c in cols]
    else:
        wells = [(r, c) for c in cols for r in rows]
    if args.p:
        fstr = "{}{:02d}"
    else:
        fstr ="{}{}"
    for w in wells[:args.n]:
        print(fstr.format(*w))

def check_range(n):
    x = int(n)
    if x < 1 or x > 96:
        raise argparse.ArgumentTypeError("{} must be an interger between 1–96".format(n))
    return x

if __name__ == "__main__":
    p = argparse.ArgumentParser(
            description="Generate plate coordinates/well labels")
    p.add_argument("-r", action="store_true",
        default=False, help="Order wells by row (default is by columns)")
    p.add_argument("-p", action="store_true",
        default=False, help="Zero-pad numbers (default is don't)")
    p.add_argument("-n", type=check_range, action="store", default=96,
        help="Stop after printing these many wells (1-96; default: 96)")
    args = p.parse_args()
    main(args)
