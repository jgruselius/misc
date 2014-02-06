# Joel Gruselius 2014
# Calculating some stats for variable 'categ' grouped by 'group1' and 'group2'
stats_by_category <- function(df, categ, group1, group2) {
	require(plyr)
		sfun <- function(x, col) {
			c(max = max(x[[col]]),
			min = min(x[[col]]),
			mean = mean(x[[col]]),
			stdev = sd(x[[col]]),
			cv = sd(x[[col]]) / mean(x[[col]]))
		}
		summary <- ddply(df, c(group1, group2), .fun=sfun, categ)
	header <- c("min", "max", "mean", "stdev", "cv")
	header <- c(group1, group2, sapply(header, paste, categ, sep="."))
		colnames(summary) <- header
		return(summary)
}