# This script finds all files with identical file names in a folder structure
# and calculates their hash

import os
import sys
import hashlib
from colorama import Fore, Back, Style

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
					# +++ REMOVE: fhash[file] = [{f: hashfile(f, hashlib.sha1())} for f in (prev, path)]
					# We assume two identically named files cannot have the same path:
					fhash[file] = {f: hashfile(f, hashlib.sha1()) for f in (prev, path)}
				else:
					# +++ REMOVE: fhash[file].append({path: hashfile(path, hashlib.sha1())})
					# We assume two identically named files cannot have the same path:
					fhash[file][path] = hashfile(path, hashlib.sha1())
			else:
				# Temporarily store path as well if filename should be encountered again:
				fnames[file] = path
	return fhash

def print_dupes(top):
	file_dict = traverse(top)
	for file, fdict in file_dict.items():
		print("{}{}{} was encountered {!s} times:".format(Fore.BLUE, file, Fore.RESET, len(fdict)))
		uniques = {}
		for path, hash in fdict.items():
			if hash in uniques:
				uniques[hash].append(path)
			else:
				uniques[hash] = [path]
		for hash, paths in uniques.items():
			print("  {}[{}]{}\t{!s} identical file(s) in:".format(Fore.RED, hash[:8], Fore.RESET, len(paths)))
			for path in paths:
				print("    {}{}/{}".format(Fore.YELLOW, os.path.split(os.path.relpath(path, start=top))[0], Fore.RESET))
		print("\n")

def print_dupes_unsorted(top):
	file_dict = traverse(top)
	for file, flist in file_dict.items():
		print("{0} was encountered {1!s} times:".format(file, len(flist)))
		for f in file_dict[file]:
			path = os.path.split("".join(f.keys()))[0] + "/"
			# Just print the first part of the hash:
			h =  "".join(f.values())[:8]
			print("{0}\n{1}".format(path, h))
		print("\n")

def hashfile(path, hasher, blocksize=65536):
	with open(path, "rb") as file:
		buf = file.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = file.read(blocksize)
	return hasher.hexdigest()

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
