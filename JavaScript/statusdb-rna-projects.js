function(doc) {
	if(doc["application"].indexOf("RNA-seq") > -1) {
		vals = ["project_name",
			"application",
			"first_initial_qc",
			"sequencing_finished",
			"close_date",
			"no_of_samples"];
		var obj = {};
		for(i in vals) {
			obj[vals[i]] = doc[vals[i]];
		}
		emit(doc["project_id"],obj);
	}
}