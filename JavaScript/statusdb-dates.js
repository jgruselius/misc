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
	var datestamp = function(dateString) {
		var d = new Date(dateString);
		if(isFinite(d)) {
			var date = [d.getFullYear(), d.getMonth()+1, d.getDate()];
			for(var i = date.length; i-->0;) { 
				var x = date[i];
				date[i] = (x > 9) ? x + '' : '0' + x;
			}
			date = date.slice(0,3).join('-'); 
		} else {
			date = null;
		}
		return date;
	};
	if(doc['entity_type'] === 'project_summary') {
		var data = {};
		data.project = doc['project_name'];
		data.app = doc['application'];
		data.n_samples = ''+doc['no_of_samples'];
		data.open_date = datestamp(doc['open_date']);
		data.close_date = datestamp(doc['close_date']);
		var x = doc['details'];
		data.sample_type = x['sample_type'];
		data.facility = x['type'];
		var prep = x['library_construction_method'];
		if(prep && prep.indexOf(',') >= 0) {
			prep = prep.replace(/,/g,"");
			prep = prep.replace(/\s\-/g,"");
			prep = prep.replace(/[\[\(][\d\-\s]+[\]\)]/g,"");
			prep = prep.trim();
		}
		data.prep = prep;
		data.lanes = ''+x['sequence_units_ordered_(lanes)'];
		data.sequencer =x['sequencing_platform'];
		data.queue_date = datestamp(x['queued']);
		data.samples_date = datestamp(x['samples_received']);
		data.order_date = datestamp(x['contract_sent']);
		data.deliver_date = datestamp(x['all_raw_data_delivered']);
		data.sequenced_date = datestamp(x['all_samples_sequenced']);
		x = doc['samples'];
		var rc_fail = 0;
		var prep_fail = 0;
		var rc_date;
		var prep_date;
		for(var s in x) {
			if(!rc_date) rc_date = datestamp(x[s]['first_initial_qc_start_date']);
			if(!prep_date) prep_date = datestamp(x[s]['first_prep_start_date']);
			var y = x[s];
			if('initial_qc' in y) {
				if(y['initial_qc']['initial_qc_status'] === 'FAILED') rc_fail++;
			}
			y = x[s]['library_prep'];
			if('A' in y) {
				if(y['A']['prep_status'] === 'FAILED') prep_fail++;
				y = y['A']['library_validation'];
				for(var z in y) {
					data.qc_date = y[z]['finish_date'];
					break;
				}
			}
		}
		data.rc_fail = ''+rc_fail;
		data.prep_fail = ''+prep_fail;
		data.rc_date = rc_date;
		data.prep_date = prep_date;
		emit(doc['_id'],data);
	}
}
