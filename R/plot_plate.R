plotPlate <- function(fileName, val="Raw.data", plateCoord="Well.positions", medianDiff=T, splitBy=NULL) {
	require(ggplot2)
	if(is.data.frame(fileName)) {
		dat <- fileName
	} else {
		if(file.exists(fileName)) {
			dat <- read.csv(file=fileName,head=T,as.is=T,na.strings=c("NA","N/A","Overflow"))
			if(length(dat) < 2) dat <- read.delim(fileName,head=T,as.is=T,na.strings=c("NA","N/A","Overflow"))
		} else {
			stop(paste("file:",fileName,"does not exist"))
		}
	}
	dat$plateRow <- substring(dat[[plateCoord]],1,1)
	dat$plateCol <- as.numeric(substring(dat[[plateCoord]],2))
	dat$numVals <- as.numeric(dat[,val])
	# Recalulate values as difference from median:
	if(medianDiff) {
		dat$numVals <- (dat$numVals-median(dat$numVals))/median(dat$numVals)
		textLabels <- sprintf("%+.2f%%",dat$numVals*100)
	} else {
		textLabels <- sprintf("%.3f",dat$numVals)
	}
	platePlot <- ggplot(data=dat,aes(x=plateCol,y=plateRow)) +
		geom_raster(aes(fill=abs(numVals)),na.rm=TRUE,interpolate=F) +
		scale_x_continuous("Column",breaks=1:12,expand=c(0,0)) +
		scale_y_discrete("Row",limits=rev(LETTERS[1:8]),expand=c(0,0)) +
		scale_fill_gradientn(colours=c("#ece7f2","#2b8cbe"),name=val) +
		geom_text(aes(label=textLabels),size=2,col="#666666") +
		theme(legend.position="none",axis.title=element_blank())
	if(!is.null(splitBy)) {
		platePlot <- platePlot + facet_grid(paste("~",splitBy,sep=""))
	}
	platePlot
}
