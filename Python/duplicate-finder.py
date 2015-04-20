# This script finds all files with identical file names in a folder structure
# and calculates their hash 

import os
import sys
import hashlib

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
					fhash[file] = [{f: hashfile(f, hashlib.sha1())} for f in (prev, path)]
				else:
					fhash[file].append({path: hashfile(path, hashlib.sha1())})
			else:
				# Temporarily store path also if filename is encountered again:
				fnames[file] = path
	for file, flist in fhash.items():
		print("{0} was encountered {1!s} times:".format(file, len(flist)))
		for f in fhash[file]:
			path = os.path.split("".join(f.keys()))[0] + "/"
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
		traverse(path)
	else:
		print("The file \"{}\" does not exist".format(path))

if __name__ == "__main__":
	main(sys.argv[1:])
