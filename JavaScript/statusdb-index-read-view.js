/*
To use this function as a CouchDB view, create a map.json file containing:
	{"map":"function(doc) { ... }"}
Remove all newline characters and make sure to use correct quoting.
The StatusDB view can then be queried by running:
	curl -s -H "Content-Type: application/json" --data "@map.json" \
	http://USER:PASS@tools-dev.scilifelab.se:5984/flowcells/_temp_view
Where USER and PASS should be replaced with the actual login details.
*/

function(doc) {
	if(doc['entity_type'] === 'flowcell_run_metrics') {
		var d = new Date(doc['creation_time']);
		var bcodes = doc['illumina']['Demultiplex_Stats']['Barcode_lane_statistics'];
		if(Object.keys(bcodes).length) {
			var yields = {};
			for(var bc in bcodes) {
				var lane = parseInt(bcodes[bc]['Lane'],10);
				var yield = bcodes[bc]['# Reads'].replace(/,/g,'');
				if(!(lane in yields)) {
					yields[lane] = {};
					var nonmatch = doc['undemultiplexed_barcodes'][lane]['undemultiplexed_barcodes']['count'];
					yields[lane]['undemuxed'] = nonmatch.reduce(function(a,b) { return (+a)+(+b); });
				}
				yields[lane][bcodes[bc]['Index']] = parseFloat(yield);
			}
			emit(doc['name'],yields);
		}
	}
}
