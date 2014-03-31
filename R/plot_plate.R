plotPlate <- function(fileName, val, plateCoord="Well", splitBy=NULL) {
	require(ggplot2)
	if(!file.exists(fileName)) {
		stop(paste("file:",fileName,"does not exist"))
	}
	dat <- read.csv(file=fileName,head=TRUE,as.is=TRUE,na.strings=c("NA","N/A"))
	dat$plateRow <- substring(dat[[plateCoord]],1,1)
	dat$plateCol <- as.numeric(substring(dat[[plateCoord]],2))
	dat$numVals <- as.numeric(dat[,val])
	platePlot <- ggplot(data=dat,aes(x=plateCol,y=plateRow)) +
		geom_tile(aes(fill=numVals,na.rm=TRUE)) +
		scale_x_continuous("Column",breaks=1:12) +
		scale_y_discrete("Row",limits=rev(LETTERS[1:8])) +
		scale_fill_gradient(low="white",high="steelblue")
	if(!is.null(splitBy)) {
		platePlot <- platePlot + facet_grid(paste("~",splitBy,sep=""))
	}
	platePlot
}
