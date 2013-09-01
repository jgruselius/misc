import sys
import untangle

# Written to convert ResequencingRunStatistics.xml from MiSeq data folder to CSV

# Replace concatenated string with file?
# Build CSV with module?

def convertSequenceStats(filePath):
	doc = untangle.parse(filePath)	
	conv = ["\n"]
	for key in doc.StatisticsResequencing.RunStats:
		conv += [val._name for val in key.get_elements()]+["\n"]
		conv += [val.cdata for val in key.get_elements()]+["\n"]
	tree = doc.StatisticsResequencing.OverallSamples.SummarizedSampleStatisics #(sic)
	conv += [key._name for key in tree[0].get_elements()]+["\n"]
	for key in tree:
		conv += [val.cdata for val in key.get_elements()]+["\n"]
	return(",".join(conv))

def main(args):
	print(convertSequenceStats(args[0]))

if __name__ == "__main__":
	main(sys.argv[1:])
