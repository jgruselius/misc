stats_by_category <- function(df, cat, group_by1, group_by2) {
	# Create an empty data frame with column names:
	headings <- c("min","max","mean","stdev","cv")
	headings <- c(group_by1,group_by2,sapply(h,paste,cat,sep="."))
	# Subset data:
	sub <- unique(df[,group_by1])
	for(i in sub) {
		sub <- unique(df[df[group_by1]==i,group_by2])
		for(j in sub) {
			vals <- df[df[group_by1]==i & df[group_by2]==j & !is.na(df[cat]),cat]
			minv <- min(vals)
			maxv <- max(vals)
			avg <- mean(vals)
			sdev <- ifelse(minv == maxv, NA, sd(vals))
			cv <- ifelse(avg == 0, NA, sdev/avg)
			newdf <- setNames(c(i,j,minv,maxv,avg,sdev,cv),headings)
			if(exists("d")) {
				d <- rbind(d,newdf)
			} else {
				d <- newdf
			}
		}
	}
	rownames(d) <- NULL
	return(as.data.frame(d))
}