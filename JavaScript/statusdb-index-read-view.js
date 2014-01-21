function(doc) {
	var d = new Date(doc['modification_time']);
	var bcodes = doc['illumina']['Demultiplex_Stats']['Barcode_lane_statistics'];
	if(d.getFullYear()==2013 && bcodes.length) {
		var yields = [];
		for(var bc in bcodes) {
			var lane = parseInt(bcodes[bc]['Lane'],10) - 1;
			var yield = bcodes[bc]['Yield (Mbases)'].replace(',','.');
			if(!(lane in yields)) {
				yields[lane] = {};
			}
			yields[lane][bcodes[bc]['Index']] = parseFloat(yield);
		}
		emit(doc['name'],yields);
	}
}
