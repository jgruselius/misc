# This script finds all files with identical file names in a folder
# structure and compares them by hash

### TODO:

import os
import sys
import argparse
import hashlib
from colorama import Fore, Back, Style
import time

# Traverses the directory tree and returns a dict mapping all file names found
# more than once to a list of path-hash pairs:
def find_dupes_by_name(paths, max_depth=None):
	fnames = {}
	fhash = {"__roots__": paths}
	n = 0
	for top in paths:
		for root, dirs, files in os.walk(top, topdown=True):
			depth = root.count(os.sep) - top.count(os.sep)
			# Stop if we have descended deeper than max_depth in the directory tree:
			if max_depth != None and depth >= max_depth:
				del dirs[:]
			for file in files:
				n += 1
				path = os.path.join(root, file)
				if file in fnames:
					# If the last encounter was the first, also add that file to
					# the collection:
					prev = fnames[file]
					if not file in fhash:
						# We assume two identically named files cannot have the same path:
						fhash[file] = {f: hashfile(f, hashlib.sha1()) for f in (prev, path)}
					else:
						# We assume two identically named files cannot have the same path:
						fhash[file][path] = hashfile(path, hashlib.sha1())
				else:
					# Temporarily store path as well if filename should be encountered again:
					fnames[file] = path
	fhash["__scanned__"] = n
	return fhash

# Base only on hash not filename:
def find_dupes_by_hash(paths, max_depth=None):
	fhash = {"__roots__": paths}
	n = 0
	for top in paths:
		for root, dirs, files in os.walk(top, topdown=True):
			depth = root.count(os.sep) - top.count(os.sep)
			# Stop if we have descended deeper than max_depth in the directory tree:
			if max_depth != None and depth >= max_depth:
				del dirs[:]
			for file in files:
				n += 1
				path = os.path.join(root, file)
				hash = hashfile(path, hashlib.sha1())
				fhash.setdefault(hash,[]).append(path)
	fhash["__scanned__"] = n
	return fhash

# Filter to size duplicates first
def find_dupes_by_size(paths, max_depth=None):
	fsize = {}
	n = 0
	for top in paths:
		for root, dirs, files in os.walk(top, topdown=True):
			depth = root.count(os.sep) - top.count(os.sep)
			# Stop if we have descended deeper than max_depth in the directory tree:
			if max_depth != None and depth >= max_depth:
				del dirs[:]
			for file in files:
				n += 1
				path = os.path.join(root, file)
				size = os.path.getsize(path)
				fsize.setdefault(size,[]).append(path)
	fhash = {"__roots__": paths}
	fhash["__scanned__"] = n
	for size, paths in fsize.items():
		if len(paths) > 1:
			for path in paths:
				hash = hashfile(path, hashlib.sha1())
				fhash.setdefault(hash,[]).append(path)
	return fhash

# Print paths for each filename grouped by hash (in color!)
def print_name_dupes(dup_obj, verbose, only_path):
	top = dup_obj.pop("__roots__")
	n_files = dup_obj.pop("__scanned__")
	n_dups = 0
	tot_size = 0
	for file, fdict in dup_obj.items():
		if verbose:
			if only_path:
				for path in fdict:
					print(path)
			else:
				print("{}{}{} was encountered {!s} times:".format(Fore.BLUE, file,
					Fore.RESET, len(fdict)))
				# Create a list of filepaths for each unique hash:
				uniques = {}
				for path, hash in fdict.items():
					if hash in uniques:
						uniques[hash].append(path)
						n_dups += 1
						tot_size += os.path.getsize(path)
					else:
						uniques[hash] = [path]
				# Print the filepaths grouped by name:
				for hash, paths in uniques.items():
					print("  {}[{}]{}\t{!s} identical file{} in:".format(Fore.RED,
						hash[:8], Fore.RESET, len(paths), "s" if len(paths)>1 else ""))
					for path in paths:
						print("	{}{}/{}".format(Fore.YELLOW,
							os.path.split(os.path.relpath(path))[0], Fore.RESET))
				print("\n")
	if not only_path:
		print("A total of {!s} duplicates ({}) could be found in {!s} scanned files\n".format(n_dups, size_format(tot_size), n_files))

# Print paths for each hash (in color!)
def print_hash_dupes(dup_obj, verbose, only_path):
	n_dups = 0
	tot_size = 0
	top = dup_obj.pop("__roots__")
	n_files = dup_obj.pop("__scanned__")
	for hash, paths in dup_obj.items():
		l = len(paths)
		if l > 1:
			n_dups += (l-1)
			tot_size += sum([os.path.getsize(f) for f in paths[1:]])
			if verbose:
				if only_path:
					for path in paths:
						print(path)
				else:
					print("{}[{}]{} ({}) was encountered {!s} times:".format(Fore.BLUE, hash[:8],
						Fore.RESET, size_format(os.path.getsize(paths[0])), l))
					for path in paths:
						print("	{}{}{}".format(Fore.YELLOW,
								os.path.relpath(path), Fore.RESET))
					print("\n")
	if not only_path:
		print("A total of {!s} duplicates ({!s}) could be found in {!s} scanned files\n".format(n_dups, size_format(tot_size), n_files))

# Print paths for each filename (ungrouped, no color)
def print_dupes_unsorted(dup_obj):
	top = dup_obj.pop("__roots__")
	for file, fdict in dup_obj.items():
		print("{0} was encountered {1!s} times:".format(file, len(fdict)))
		for path, hash in fdict.items():
			print("{0}/\n{1}".format(os.path.split(os.path.relpath(path))[0], hash[:8]))
		print("\n")

def hashfile(path, hasher, blocksize=65536):
	with open(path, "rb") as file:
		buf = file.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = file.read(blocksize)
	return hasher.hexdigest()

def benchmark(paths, n=99):
	dup_obj = find_dupes_by_name(paths)
	temp = sys.stdout
	sys.stdout = None
	res = []
	for f in (print_dupes, print_dupes_unsorted):
		t0 = time.clock()
		for i in range(n):
			f(dup_obj)
		t1 = time.clock() - t0
		res.append("{}: {:.3f}s ({:.5f}s per iteration)\n".format(f.__name__, t1, t1/n))
	sys.stdout = temp
	print("".join(res))

def size_format(num, suffix="B"):
	for unit in ["","Ki","Mi","Gi","Ti","Pi","Ei","Zi"]:
		if abs(num) < 1024.0:
			return "{:.2f} {}{}".format(num, unit, suffix)
		num /= 1024.0
	return "{:.2f}{}{}".format(num, 'Yi', suffix)

def main(args):
	paths = [os.path.abspath(os.path.expanduser(os.path.normpath(p))) for p in args.paths]
	bad_paths = [p for p in paths if not os.path.exists(p)]
	if bad_paths:
		for p in bad_paths:
			print("The directory \"{}\" does not exist".format(p))
	else:
		if args.name:
			print_name_dupes(find_dupes_by_name(paths, args.depth), args.sum, args.pathonly)
		elif args.nosize:
			print_hash_dupes(find_dupes_by_hash(paths, args.depth), args.sum, args.pathonly)
		else:
			print_hash_dupes(find_dupes_by_size(paths, args.depth), args.sum, args.pathonly)

if __name__ == "__main__":
	p = argparse.ArgumentParser(description="""Find duplicate files by hash,
	    by default only compare the hash of files which size is identical""")
	p.add_argument("paths", nargs="+",
		help="All paths to compare files in")
	p.add_argument("--depth", type=int, action="store", default=None,
	    help="Max depth to traverse (default = no limit)")
	g = p.add_mutually_exclusive_group()
	g.add_argument("--nosize", action="store_true", default=False,
		help="Compare all files regardless of size (not recommended)")
	g.add_argument("--name", action="store_true", default=False,
		help="Only compare files with identical names")
	h = p.add_mutually_exclusive_group()
	h.add_argument("--sum", action="store_false", default=True,
		help="Only print summary of search")
	h.add_argument("--pathonly", action="store_true", default=False,
		help="Only print path of duplicate files, one per line")
	args = p.parse_args()
	main(args)
