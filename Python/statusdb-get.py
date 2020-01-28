#! /usr/bin/env python

import sys
import json
import csv
import re
import requests
import getpass
import argparse
import collections


def get_data(url, js_path):
    user = input("User name for {0}: ".format(url))
    passw = getpass.getpass("Password: ")

    with open(js_path) as js_file:
        js = js_file.read()

    ### Format JavaScript ###
    # Replace newlines and remove tabs:
    js = js.replace("\n", " ")
    js = js.replace("\t", "")
    # Remove JS comments:
    js = re.sub("(\/\*)[^\*]+\*\/", "", js).strip()

    ### Request data with POST ###
    post_data = json.dumps({"map": js})
    header = {"content-type": "application/json"}
    response = requests.post(url, headers=header, auth=(user, passw),
                             data=post_data, stream=True)
    return response


def write_json(resp, out_file):
    for line in resp.iter_lines(decode_unicode=True):
        out_file.write(line)

def write_simple_json(resp, out_file):
    def _simplify():
        obj = resp.json()
        for row in obj["rows"]:
            key = row["key"]
            value = row["value"]
            yield json.dumps({key: value})

    for line in _simplify():
        out_file.write("{}\n".format(line))

def flatten(l):
    for val in l.values() if isinstance(l, dict) else l:
        if isinstance(val, (tuple, list)):
            for sub in flatten(val):
                yield sub
        elif isinstance(val, dict):
            for sub in flatten(val.values()):
                yield sub
        else:
            yield val


def write_csv_gen(resp, out_file):
    writer = csv.writer(out_file, delimiter=",")
    # writer.writerow(header)
    # Parse using for loop:
    # header = None
    # for line in resp.iter_lines(decode_unicode=True):
    #   if re.match("\{\"id", line):
    #       obj = json.loads(line.rstrip("\r\n,"))
    #       if not header:
    #           header = ["key"]
    #           header.extend([key for key in obj["value"].keys()])
    #           writer.writerow(header)
    #       row = [obj["key"]]
    #       row.extend([val for val in obj["value"].values()])
    #       writer.writerow(row)

    # Parse using generator function:
    def _csv_gen():
        p = re.compile(r"\{\"id")
        for line in resp.iter_lines(decode_unicode=True):
            if p.match(line):
                obj = json.loads(line.rstrip("\r\n,"))
                row = [obj["key"]]
                vals = obj["value"]
                row.extend(flatten(vals))
                yield row

    writer.writerows(_csv_gen())

# CSV formatter for reads per barcode data:
def write_custom1(resp, out_file):
    # Data object is of format:
    #   Total flowcells:    data["total_rows"]
    #   Offset:             data["offset"]
    #   Flowcell data:      data["rows"]
    # Where data["rows"] is a list and if fc = data["rows"][n]:
    #   Database hash key:  fc["id"]
    #   Flowcell/run ID:    fc["key"]
    #   Lane data:          fc["value"]
    # Where fc["value"] is a list and if n is the lane index then
    # fc["value"][n-1] is of format {barcode_sequence : million_reads}

    # Write comma-separated output with format RUN_ID,LANE,BARCODE,READS:
    writer = csv.writer(out_file, delimiter=",")
    writer.writerow(["RUN_ID", "LANE", "BARCODE", "READS"])
    p = re.compile(r"\{\"id")
    for line in resp.iter_lines(decode_unicode=True):
        if p.match(line):
            fc = json.loads(line.rstrip("\r\n,"))
            writer.writerows([[fc["key"], i, bc, reads]
                             for i, lane in fc["value"].items()
                             for bc, reads in lane.items()])
# CSV formatter for date data:
def write_custom2(resp, out_file):
    header = ["project","app","facility","sample_type","prep",
        "n_samples","rc_fail","prep_fail","lanes","sequencer","open_date",
        "close_date","queue_date","samples_date","sequenced_date","deliver_date"
        ,"prep_date","qc_date","rc_date","order_date"]
    obj = resp.json()
    s = "\t".join(header)
    out_file.write("{}\n".format(s))
    for e in obj["rows"]:
        row = []
        vals = e["value"]
        for x in header:
            if x in vals and vals[x] != None and vals[x] != "undefined":
                row.append(vals[x])
            else:
                row.append("")
        s = "\t".join(row)
        out_file.write("{}\n".format(s))

# CSV formatter for fragment size data:
def write_custom3(resp, out_file):
    writer = csv.writer(out_file, delimiter=",")
    header = ["proj", "app" ,"open", "lib", "prep", "sample", "size", "nm"]
    obj = resp.json()
    writer.writerow(header)
    for e in obj["rows"]:
        vals = e["value"]
        for k,v in vals["samples"].items():
            row = [vals[x] for x in header[:-3]] + [k, v["size"], v["nm"]]
            writer.writerow(row)

# CSV formatter for flowcell data:
def write_custom4(resp, out_file):
    writer = csv.writer(out_file, delimiter=",")
    header = ["date", "flowcell", "sequencer", "lane", "barcode", "project", "sample" ,"reads"]
    writer.writerow(header)
    p = re.compile(r"\{\"id")
    for line in resp.iter_lines(decode_unicode=True):
        if p.match(line):
            obj = json.loads(line.rstrip("\r\n,"))
            vals = obj["value"]
            pre = [vals[x] for x in header[:3]]
            for lane, barcodes in vals["lanes"].items():
                for bc, data in barcodes.items():
                    writer.writerow(pre + [lane, bc] + [data[x] for x in header[-3:]])


if __name__ == "__main__":
    # Parse command-line arguments:
    parser = argparse.ArgumentParser(description="Query a CouchDB database")
    parser.add_argument("jsfile", help="File containing JavaScript map function")
    parser.add_argument("--out", help="File to write response to (default: stdout")
    parser.add_argument("--url", help="Database URL", default="http://tools-dev.scilifelab.se:5984/projects/_temp_view")
    parser.add_argument("--csv", help="Convert response to CSV", action="store_true")
    parser.add_argument("-s", "--simplify", help="Omit database id's", action="store_true")
    args = parser.parse_args()

    if args.csv:
        write_func = write_csv_gen
    else:
        if args.simplify:
            write_func = write_simple_json
        else:
            write_func = write_json

    write_func = write_custom2
    resp = get_data(args.url, args.jsfile)

    if args.out:
        with open(args.out, "w") as out_file:
            write_func(resp, out_file)
    else:
        write_func(resp, sys.stdout)
