/*
 Joel Gruselius, 2012

 (Google Apps script)

 ~~Description~~

*/

function performanceTest() {
	var testSet = constructTestSet(1000, 6);
	var times = new Array(3);
	times[0] = new Date().getTime();
	evaluateIndexes1(testSet);
	times[1] = new Date().getTime();
	evaluateIndexes2(testSet);
	times[2] = new Date().getTime();
	return times;
}

/*
 Converts a two-dimensional array A[m][n] to a one-dimensional A[m]
*/
function flattenArray(arr) {
	var newArr = new Array(arr.length);
	for(var i = 0, n = arr.length; i < n; i++) {
		newArr[i] = arr[i][0];
	}
	return newArr;
}

/*
 Find all indexes that are compatible with the given one(s)  
*/
function findCompatibles(indexSequences) {
	var str = "";
	if(typeof indexSequences == "string") {
		indexSequences = [indexSequences];
	} else {
		indexSequences = flattenArray(indexSequences);
	}
	for(var index in indexReference) {
	if(evaluateIndexes(indexSequences.concat(indexReference[index]))) {
		str += index + " ";
	}
	}
	return str;
}

/*
 Convert an array of index codes to the actual index sequences:
*/
function indexLookup(codes) {
	var seqs = new Array(codes.length);
	var seq; 
	for(var i = 0, n = codes.length; i < n; i++) {
		seq = indexTable(codes[i]);
		if(typeof seq === "undefined") {
			throw "UnknownIndexCodeExceeption";
		} else {
			seqs[i] = seq;
		}
	}
	return seqs;
}

/*
 Constructs an array of 'size' strings with randomized sequences 
 of 'length' characters A, C, T, G.
*/
function constructTestSet(size, length) {
	var set = new Array(size);
	var map = ["A","C","T","G"];
	var seq;
	for(var i = 0, n = size; i < n; i++) {
		seq = "";
		var x;
		for(var j = 0, m = length; j < m; j++) {
			x = Math.floor((Math.random()*4));
			seq += map[x];
		}
		set[i] = seq;
	}
	return set;
}

function evaluateIndexes1(indexList) {
	verifySequences(indexList);
	var channelSeqs = new Array(indexList.length);
	for(var i = 0, n = indexList.length; i < n ; i++) {
		channelSeqs[i] = convertToBinaryChannel(indexList[i]);
	}
	return bitwiseCompabilityCheck(channelSeqs);
}

function evaluateIndexes2(indexList) {
	verifySequences(indexList);
	return charCountCompabilityCheck(indexList);
}

/*
 Iterates over all strings in 'seqs' and verifies they are of equal lenght, 
 only contain characters A, T, C, G and converts them to upper-case.
*/
function verifySequences(seqs) {
	var pattern = /[^ATGC]/i;
	var size = seqs[0].length;
	var seq;
	for(var i = 0, n = seqs.length; i < n ; i++) {
		seq = seqs[i];
		if(pattern.test(seq) || seqs[i].length != size) {
			throw "InvalidSequenceException";
		} else {
			seqs[i] = seq.toUpperCase();
		}
	}
}

function bitwiseCompabilityCheck(list) {
	var len = list[0].length;
	var zeroMask = 0;
	var oneMask = Math.pow(2, len) - 1;
	var arr;
	/*
	 If an array of strings are supplied rather than integers,
	 convert strings representing binary integers:
	*/
	if(typeof list[0] == "string") {
		arr = new Array(list.length);
		for(var i = 0, n = list.length; i < n ; i++) {
			arr[i] = parseInt(list[i], 2);
		}
	} else { 
		arr = list; 
	}
	var zeroCheck = zeroMask;
	var oneCheck = oneMask;
	var bin;
	for(var i = 0, n = arr.length; i < n ; i++) {
		bin = arr[i];
		zeroCheck |= bin;
		oneCheck &= bin;
	}
	/*
	A zero bit in 'zeroCheck' means all bits in that position are zero,
	using XOR against a one-mask will then give non-zero

	A one bit in 'oneCheck' means all bits in that position are one,
	using XOR against a zero-mask will then give non-zero 
	*/
	return ((oneMask ^ zeroCheck) + (zeroMask ^ oneCheck) == 0);
}

/*
 Constructs a string describing the channel used for each nucleotide in a 
 sequence, e.g. 'ATCTG' returns "10100".
*/
function convertToBinaryChannel(seq, method) {
	var chan = "";
	var num;
	// Method 1, using regexp and String.replace():
	if(method === 1 || typeof method === "undefined") {
		// G, T uses green laser denoted '0':
		chan = seq.replace(/(g|t)/gi,"0");
		// A, C uses red laser denoted '1':
		chan = chan.replace(/(a|c)/gi,"1");
	}

	// Method 2 builds a string but does not use regexp:
	else if(method === 2) {
		var base;
		for(var i = 0, n = seq.length; i < n ; i++) {
			base = seq[i];
			// G, T uses green laser denoted '0':
			if(base == "G" || base == "T") { chan += "0"; }
			// A, C uses red laser denoted '1':
			else if(base == "A" || base == "C") { chan += "1" };
		}
	} 
	// Method 3 calculates the binary integer directly:
	else if(method === 3) {
		var base;
		for(var i = 0, n = seq.length; i < n ; i++) {
			base = seq[i];
			// G, T uses green laser denoted '0':
			// A, C uses red laser denoted '1':
			if(base == "A" || base == "C") { num += Math.pow(2,n-i-1); }
		}
	}

	return chan;
}

/* 
 This method is much more readable than the bitwise alternative but not as much fun ;(
*/
function charCountCompabilityCheck(seqs) {
	var positionArray = new Array(seqs[0].length);
	// Create a base counter for each position:
	for(var i = 0, n = seqs[0].length; i < n; i++) {
		positionArray[i] = {A:0, T:0, G:0, C:0};
	}
	// Iterate over all sequences:
	var seq;
	for(var i = 0, n = seqs.length; i < n ; i++) {
		seq = seqs[i];
		// Iterate over all positions in current sequence:
		for(var j = 0, m = seq.length; j < m; j++) {
			// Add one to the count for the base in this position:
			positionArray[j][seq[j]] += 1;
		}
	}
	// Sum channel distribution:
	var green;
	var red;
	for(var i = 0, n = seqs[0].length; i < n ; i++) {
		green = positionArray[i].T + positionArray[i].G;
		red = positionArray[i].A + positionArray[i].C;
	}
	return (green > 0 && red > 0);
}

/*
 This list was taken from PerK 2012-06-28
*/
var indexReference = {
	"a1":"ATCACG",
	"a2":"CGATGT",
	"a3":"TTAGGC",
	"a4":"TGACCA",
	"a5":"ACAGTG",
	"a6":"GCCAAT",
	"a7":"CAGATC",
	"a8":"ACTTGA",
	"a9":"GATCAG",
	"a10":"TAGCTT",
	"a11":"GGCTAC",
	"a12":"CTTGTA",
	"a13":"AAACAT",
	"a14":"CAAAAG",
	"a15":"GAAACC",
	"a16":"TAATCG",
	"a17":"AAAGCA",
	"a18":"CAACTA",
	"a19":"GAATAA",
	"a20":"TACAGC",
	"a21":"AAATGC",
	"a22":"CACCGG",
	"a23":"GACGGA",
	"a24":"AGGCCG",
	"a25":"AACAAA",
	"a26":"CACGAT",
	"a27":"GATATA",
	"a28":"TATAAT",
	"a29":"AACCCC",
	"a30":"CACTCA",
	"a31":"GATGCT",
	"a32":"TCATTC",
	"a33":"AACTTG",
	"a34":"CAGGCG",
	"a35":"GCAAGG",
	"a36":"ATAATT",
	"a37":"AAGACT",
	"a38":"CATGGC",
	"a39":"GCACTT",
	"a40":"TCCCGA",
	"a41":"AAGCGA",
	"a42":"CATTTT",
	"a43":"GCCGCG",
	"a44":"TCGAAG",
	"a45":"AAGGAC",
	"a46":"CCAACA",
	"a47":"GCCTTA",
	"a48":"ATACGG",
	"a49":"AATAGG",
	"a50":"CCACGC",
	"a51":"GCTCCA",
	"a52":"TCGGCA",
	"a53":"ACAAAC",
	"a54":"CCCATG",
	"a55":"GGCACA",
	"a56":"TCTACC",
	"a57":"ACATCT",
	"a58":"CCCCCT",
	"a59":"GGCCTG",
	"a60":"ATCCTA",
	"a61":"ACCCAG",
	"a62":"CCGCAA",
	"a63":"GTAGAG",
	"a64":"TGAATG",
	"a65":"ACCGGC",
	"a66":"CCTTAG",
	"a67":"GTCCGC",
	"a68":"TGCCAT",
	"a69":"ACGATA",
	"a70":"CGAGAA",
	"a71":"GTGAAA",
	"a72":"ATCTAT",
	"a73":"ACTCTC",
	"a74":"CGGAAT",
	"a75":"GTGGCC",
	"a76":"TGCTGG",
	"a77":"ACTGAT",
	"a78":"CTAGCT",
	"a79":"GTTTCG",
	"a80":"TGGCGC",
	"a81":"AGAAGA",
	"a82":"CTATAC",
	"a83":"CGTACG",
	"a84":"ATGAGC",
	"a85":"AGATAG",
	"a86":"CTCAGA",
	"a87":"GAGTGG",
	"a88":"TTCGAA",
	"a89":"AGCATC",
	"a90":"CTGCTG",
	"a91":"GGTAGC",
	"a92":"TTCTCC",
	"a93":"AGCGCT",
	"a94":"CCGTCC",
	"a95":"ATTCCT",
	"a96":"AGGTTT",
	"h1":"CTCGGT",
	"h2":"AATCGT",
	"h3":"GCGCGT",
	"h4":"CGAAGT",
	"h5":"TATTCT",
	"h6":"AGATCT",
	"h7":"CAGGCT",
	"h8":"TCCGCT",
	"h9":"GGTCCT",
	"h10":"TCGTAT",
	"h11":"GTCCAT",
	"h12":"GATTGG",
	"h13":"TTACGG",
	"h14":"CCTTCG",
	"h15":"GGAGCG",
	"h16":"ACGCAG",
	"h17":"TGCCAG",
	"h18":"GAGAAG",
	"h19":"ATCAAG",
	"h20":"CGATTC",
	"h21":"ACCGTC",
	"h22":"TAAGTC",
	"h23":"TTCATC",
	"h24":"AGCAGC",
	"h25":"GCGTCC",
	"h26":"AGGTAC",
	"h27":"ACGTTA",
	"h28":"AACCTA",
	"h29":"TGGATA",
	"h30":"TTATCA",
	"h31":"ATAGAA",
	"h32":"CTGGTT",
	"h33":"GGAGTT",
	"h34":"TACCTT",
	"h35":"TCTACT",
	"h36":"ATAACT",
	"h37":"GAGTAT",
	"h38":"AGCTAT",
	"h39":"CAAGAT",
	"h40":"TCGTTG",
	"h41":"ACTCTG",
	"h42":"GATATG",
	"h43":"TATGCG",
	"h44":"GTACCG",
	"h45":"CAGACG",
	"h46":"CCTGAG",
	"h47":"TATTGC",
	"h48":"GAGAGC",
	"h49":"ATATAC",
	"h50":"GCCGAC",
	"h51":"CTTAAC",
	"h52":"GTTCTA",
	"h53":"CAGCTA",
	"h54":"ACCGGA",
	"h55":"CTCCGA",
	"h56":"TTAAGA",
	"h57":"GGTTCA",
	"h58":"ACGCCA",
	"h59":"CGACCA",
	"h60":"TCGGAA",
	"h61":"GGCCTT",
	"h62":"AGACGT",
	"h63":"CATAGT",
	"h64":"GATGAT",
	"h65":"CCTATG",
	"h66":"AACTGG",
	"h67":"GCGAGG",
	"h68":"TTCTCG",
	"h69":"GCTGCG",
	"h70":"CTGGCG",
	"h71":"CGAACG",
	"h72":"ATTCAG",
	"h73":"CCGTTC",
	"h74":"TACTTC",
	"h75":"GAGGTC",
	"h76":"ATCCTC",
	"h77":"TCAATC",
	"h78":"CTTCGC",
	"h79":"GACCGC",
	"h80":"ATAAGC",
	"h81":"CATTAC",
	"h82":"TGATAC",
	"h83":"CTAGAC",
	"h84":"TAGAAC",
	"h85":"ATGGTA",
	"h86":"GTACGA",
	"h87":"AAGAGA",
	"h88":"GGCAGA",
	"h89":"GGAGAA",
	"h90":"GCGCAA",
	"h91":"GCGGTT",
	"h92":"TTAGTT",
	"h93":"AGAATT",
	"h94":"ATCAGT",
	"h95":"GGCGCT",
	"h96":"ACTTAT",
	"1":"ATCACG",
	"2":"CGATGT",
	"3":"TTAGGC",
	"4":"TGACCA",
	"5":"ACAGTG",
	"6":"GCCAAT",
	"7":"CAGATC",
	"8":"ACTTGA",
	"9":"GATCAG",
	"10":"TAGCTT",
	"11":"GGCTAC",
	"12":"CTTGTA",
	"13":"AGTCAA",
	"14":"AGTTCC",
	"15":"ATGTCA",
	"16":"CCGTCC",
	"18":"GTCCGC",
	"19":"GTGAAA",
	"20":"GTGGCC",
	"21":"GTTTCG",
	"22":"CGTACG",
	"23":"GAGTGG",
	"25":"ACTGAT",
	"27":"ATTCCT",
	"m1":"AAGGGA",
	"m2":"CCTTCA",
	"m3":"GGACCC",
	"m4":"TTCAGC",
	"m5":"AAGACG",
	"m6":"CCTCGG",
	"m7":"GGATGT",
	"m8":"TTCGCT",
	"m9":"ACACGA",
	"m10":"CACACA",
	"m11":"GTGTTA",
	"m12":"TGTGAA",
	"m13":"ACAAAC",
	"m14":"CACCTC",
	"m15":"GTGGCC",
	"m16":"TGTTGC",
	"r1":"ATCACG",
	"r2":"CGATGT",
	"r3":"TTAGGC",
	"r4":"TGACCA",
	"r5":"ACAGTG",
	"r6":"GCCAAT",
	"r7":"CAGATC",
	"r8":"ACTTGA",
	"r9":"GATCAG",
	"r10":"TAGCTT",
	"r11":"GGCTAC",
	"r12":"CTTGTA",
	"r13":"AGTCAA",
	"r14":"AGTTCC",
	"r15":"ATGTCA",
	"r16":"CCGTCC",
	"r17":"GTAGAG",
	"r18":"GTCCGC",
	"r19":"GTGAAA",
	"r20":"GTGGCC",
	"r21":"GTTTCG",
	"r22":"CGTACG",
	"r23":"GAGTGG",
	"r24":"GGTAGC",
	"r25":"ACTGAT",
	"r26":"ATGAGC",
	"r27":"ATTCCT",
	"r28":"CAAAAG",
	"r29":"CAACTA",
	"r30":"CACCGG",
	"r31":"CACGAT",
	"r32":"CACTCA",
	"r33":"CAGGCG",
	"r34":"CATGGC",
	"r35":"CATTTT",
	"r36":"CAAACA",
	"r37":"CGGAAT",
	"r38":"CTAGCT",
	"r39":"CTATAC",
	"r40":"CTCAGA",
	"r41":"GACGAC",
	"r42":"TAATCG",
	"r43":"TACAGC",
	"r44":"TATAAT",
	"r45":"TCATTC",
	"r46":"TCCCGA",
	"r47":"TCGAAG",
	"r48":"TCGGCA"
};