# This script finds all files with identical file names in a folder structure
# and compares them by hash

import os
import sys
import hashlib
from colorama import Fore, Back, Style
import time

# Traverses the directory tree and returns a dict mapping all file names found
# more than once to a list of path-hash pairs:
def traverse(top):
	fnames = {}
	fhash = {}
	for root, dirs, files in os.walk(top, topdown=False):
		for file in files:
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
	return fhash

# Print paths for each filename grouped by hash (in color!)
def print_dupes(top):
	file_dict = traverse(top)
	for file, fdict in file_dict.items():
		print("{}{}{} was encountered {!s} times:".format(Fore.BLUE, file,
			Fore.RESET, len(fdict)))
		# Create a list of filepaths for each unique hash:
		uniques = {}
		for path, hash in fdict.items():
			if hash in uniques:
				uniques[hash].append(path)
			else:
				uniques[hash] = [path]
		# Print the filepaths grouped by hash:
		for hash, paths in uniques.items():
			print("  {}[{}]{}\t{!s} identical file{} in:".format(Fore.RED,
				hash[:8], Fore.RESET, len(paths), "s" if len(paths)>1 else ""))
			for path in paths:
				print("    {}{}/{}".format(Fore.YELLOW,
					os.path.split(os.path.relpath(path, start=top))[0],
						Fore.RESET))
		print("\n")

# Print paths for each filename (ungrouped, no color)
def print_dupes_unsorted(top):
	file_dict = traverse(top)
	for file, fdict in file_dict.items():
		print("{0} was encountered {1!s} times:".format(file, len(fdict)))
		for path, hash in fdict.items():
			print("{0}/\n{1}".format(os.path.split(os.path.relpath(path, start=top))[0], hash[:8]))
		print("\n")

def hashfile(path, hasher, blocksize=65536):
	with open(path, "rb") as file:
		buf = file.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = file.read(blocksize)
	return hasher.hexdigest()

def benchmark(path, n=99):
	temp = sys.stdout
	sys.stdout = None
	res = []
	for f in (print_dupes, print_dupes_unsorted):
		t0 = time.clock()
		for i in range(n):
			f(path)
		t1 = time.clock() - t0
		res.append("{}: {:.3f}s ({:.5f}s per iteration)\n".format(f.__name__, t1, t1/n))
	sys.stdout = temp
	print("".join(res))

def main(args):
	path = os.path.abspath(os.path.expanduser(os.path.normpath(args[0])))
	if os.path.exists(path):
		print_dupes(path)
	else:
		print("The directory \"{}\" does not exist".format(path))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage:\n\tpython {0} <dir>".format(os.path.basename(sys.argv[0])))
	else:
		main(sys.argv[1:])
