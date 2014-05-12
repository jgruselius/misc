# Joel Gruselius 2014
# Calculating some stats for variable 'categ' grouped by 'group1' and 'group2'
# Set na.rm=TRUE to only use complete rows of df (i.e. rows with no missing 
# value in any column)
stats_by_category <- function(df, categ, group1, group2=NULL, na.rm=FALSE) {
	require(plyr)
	sfun <- function(x, col) {
		num <- as.numeric(x[[col]])
		c(count  = length(num),
		  min    = min(num),
		  max    = max(num),
		  mean   = mean(num),
		  median = median(num),
		  sum    = sum(num),
		  stdev  = sd(num),
		  cv     = sd(num) / mean(num))
	}
	if(na.rm) df <- df[complete.cases(df[,c(categ, group1, group2)]),]
	summary <- ddply(df, c(group1, group2), .fun=sfun, categ)
	header <- c("min", "max", "mean", "median", "sum", "stdev", "cv")
	header <- c(group1, group2, "count", sapply(header, paste, categ, sep="."))
	colnames(summary) <- header
	return(summary)
}