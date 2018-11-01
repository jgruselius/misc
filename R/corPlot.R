corPlot <- function(df, square=FALSE, method="pearson", type=1) {
	df_num <- df[sapply(df, is.numeric)]
	cors <- as.data.frame(cor(df_num, method=method,use="pairwise.complete.obs"))
	cors <- cors[rowSums(is.na(cors))<2, colSums(is.na(cors))<2]
	cors <- get_lower_tri(cors)
	if(square) { 
		cors <- "^"(cors, 2)
	} else {
		cors <- as.matrix(abs(cors))
	}
	if(type==2) {
		#require(ggplot2, reshape2)
		cors <- melt(cors, na.rm=T)
		ggplot(cors, aes(Var1, Var2, fill=value)) + geom_tile() +
			geom_text(size=2, aes(label=round(value, 2))) +
			ylab("") + xlab("") + scale_fill_continuous(name=paste(method, "coef")) +
			theme_bw() +
			theme(axis.text.x=element_text(angle=45, hjust=1, vjust=1))
	} else if(type==3) {
		# The order of the axis labels is incorrect!
		message("WARNING: The order of the axis labels is incorrect!")
		require(plotly)
		plot_ly(x=rownames(cors), y=colnames(cors), z=cors, type="heatmap")
	} else {
		heatmap(cors, Rowv=NA, Colv=NA, heat.colors(256), symm=T)
	}
}

# Two functions below from http://www.sthda.com/english/wiki/ggplot2-quick-correlation-matrix-heatmap-r-software-and-data-visualization

# Set upper triangle of the correlation matrix to NA
get_lower_tri <- function(cormat) {
	cormat[upper.tri(cormat)] <- NA
	return(cormat)
}

reorder_cormat <- function(cormat) {
	# Use correlation between variables as distance
	dd <- as.dist((1-cormat)/2)
	hc <- hclust(dd)
	cormat <-cormat[hc$order, hc$order]
}