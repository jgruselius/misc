import sys
import inspect
import ba_parser

def main(args):
	reader = ba_parser.BioanalyzerParser()
	if len(args) == 1:
		reader.loadFile(args[0])
		reader.parseFile()
	else:
		print "Usage:\n\tpython %s <input_file> [output_file]\n" % __file__

if __name__ == "__main__":
	main(sys.argv[1:])