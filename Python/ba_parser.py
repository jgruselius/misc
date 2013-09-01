import csv
import re

class BioanalyzerParser:
	inputFile = None

	def __init__(self):
		pass
	
	def loadFile(self, inputFileName):
		try:
			self.inputFile = open(inputFileName, "rb")
		except IOError:
			raise

	def parseFile(self):
		if not self.inputFile:
			raise ParserException("No inputfile loaded")
		csv_reader = csv.reader(self.inputFile, delimiter=",",
			quoting=csv.QUOTE_MINIMAL)
		rowlist = []
		for row in csv_reader:
			rowString = "".join(row)
			# Don't add empty or all-whitespace rows:
			if not re.search("^\s*$", rowString):
				print row
				rowlist.append(row)
		# (We could combine above and below...)
		# Now create a dictionary for with sample names as keys:
		sampleData = {}
		for row in rowlist:
			if row[0] == "Sample Name":
				sampleData[row[1]] = {}

	def __del__(self):
		if self.inputFile: self.inputFile.close()

class ParserException:
	message = None
	
	def __init__(self, message=""):
		self.message = message
		
	def __str__(self):
		return repr(self.message)