function onOpen(e) {
	SpreadsheetApp.getUi().createAddonMenu()
		.addItem('Reverse', 'wReverse')
		.addItem('Complement', 'wComplement')
		.addItem('Reverse complement', 'wReverseComplement')
		.addItem('Translate', 'wTranslate')
	.addToUi();
}

function onInstall(e) {
	onOpen(e);
}

function wReverse() {
	rangeApply(reverse);
}

function wComplement() {
	rangeApply(complement);
}

function wReverseComplement() {
	rangeApply(reverseComplement);
}

function wTranslate() {
	rangeApply(translate);
}

function showAlert(msg) {
	SpreadsheetApp.getUi().alert("There was an error!", msg);
}

function define() {
}

define.COMPL_MAP = {'A':'T','T':'A','C':'G','G':'C'};
define.CODON_MAP = {
	'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
	'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
	'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
	'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
	'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
	'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
	'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
	'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
	'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
	'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
	'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
	'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
	'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
	'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
	'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
	'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
	};

function rangeApply(func) {
	var range = SpreadsheetApp.getActive().getActiveRange();
	var vals = range.getValues();
	var cols = range.getNumColumns();
	var rows = range.getNumRows();

	for(var i=0; i<rows; i++) {
		for(var j=0; j<cols; j++) {
			var val = vals[i][j];
			if(typeof val === "string") {
				val = clean(val);
				if(isSeq(val)) {
					vals[i][j] = func(val);
				}
			}
		}
	}
	range.setValues(vals);
}

// Remove whitespace and convert to uppercase
function clean(str) {
	return str.replace(/\s+/g,"").toUpperCase();
}

function isSeq(str) {
	return !(str.match(/[^ATGC]/g));
}

function reverse(seq) {
	return seq.split("").reverse().join("");
}

function complement(seq) {
	var CMAP = define.COMPL_MAP;
	return seq.split("").map(function(x) { return CMAP[x]; }).join("");
}

function reverseComplement(seq) {
	var CMAP = define.COMPL_MAP;
	return seq.split("").reverse().map(function(x) { return CMAP[x]; }).join("");
}

function translate(seq) {
	// Split the string into three letter chunks:
	var n = Math.ceil(seq.length/3);
	var codons = new Array(n);
	for(var i=0; i<n; i++) {
		codons[i] = seq.substr(i*3,3);
	}
	var CODON_MAP = define.CODON_MAP;
	return codons.map(function(x) { return CODON_MAP[x]; }).join("");
}