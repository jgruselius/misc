plotPlate <- function(fileName, val, plateCoord="Well", splitBy=NULL) {
	require(ggplot2)
	if(is.data.frame(fileName)) {
		dat <- fileName
	} else {
		if(file.exists(fileName)) {
			dat <- read.csv(file=fileName,head=T,as.is=T,na.strings=c("NA","N/A","Overflow"))
		} else {
			stop(paste("file:",fileName,"does not exist"))
		}
	}
	dat$plateRow <- substring(dat[[plateCoord]],1,1)
	dat$plateCol <- as.numeric(substring(dat[[plateCoord]],2))
	dat$numVals <- as.numeric(dat[,val])
	platePlot <- ggplot(data=dat,aes(x=plateCol,y=plateRow)) +
		geom_tile(aes(fill=numVals,na.rm=TRUE)) +
		scale_x_continuous("Column",breaks=1:12) +
		scale_y_discrete("Row",limits=rev(LETTERS[1:8])) +
		scale_fill_gradient(low="white",high="steelblue",name=val) +
		geom_text(aes(label=signif(numVals,3)),size=2,col="#666666")
	if(!is.null(splitBy)) {
		platePlot <- platePlot + facet_grid(paste("~",splitBy,sep=""))
	}
	platePlot
}
