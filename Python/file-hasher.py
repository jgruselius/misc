import os
import hashlib

def file_hash(path):
	for name in os.listdir(path):
		file = os.path.join(path, name)
		if os.path.isfile(file):
			yield (os.path.basename(file), hashfile(file, hashlib.sha1()))
	#return ((f, hashfile(f)) for f in os.listdir(path) if os.path.isfile(f))

def hashfile(path, hasher, blocksize=65536):
	with open(path, "rb") as file:
		buf = file.read(blocksize)
		while len(buf) > 0:
			hasher.update(buf)
			buf = file.read(blocksize)
	return hasher.hexdigest()

def compare_dirs(path1, path2):
	f1 = file_hash(path1)
	f2 = file_hash(path2)
	for pair in zip(f1, f2):
		if(f1[1] == f2[1]):
			pass
		else:
			pass
