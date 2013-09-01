sum_data_per_lane <- function(data) {
	runs <- unique(data$Description)
	for(r in runs) {
		print(r)
		run_data <- data[data$Description==r,]
		lanes <- unique(run_data$Lane)
		for(l in lanes) {
			print(sum(run_data[run_data$Lane==l,]$Read.pairs..Mbases.))
		}
	}
}