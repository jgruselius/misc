stats_by_category <- function(df, cat, group_by1, group_by2) {
	d <- data.frame()
	sub <- unique(df[,group_by1])
	for(i in sub) {
		sub <- unique(df[df[group_by1]==i,group_by2])
		for(j in sub) {
			vals <- df[df[group_by1]==i & df[group_by2]==j,]
			avg <- mean(vals[!is.na(vals[cat]),cat])
			sdev <- sd(vals[!is.na(vals[cat]),cat])
			cv <- sdev/avg
			h1 <- paste(cat,"mean",sep=".")
			h2 <- paste(cat,"stdev",sep=".")
			h3 <- paste(cat,"cv",sep=".")
			d <- rbind(d,data.frame(group_by1=i,group_by2=j,h1=avg,h2=sdev,h3=cv))
		}
	}
	names(d)[1] <- group_by1
	names(d)[2] <- group_by2
	names(d)[3] <- h1
	names(d)[4] <- h2
	names(d)[5] <- h3
	return(d)
}