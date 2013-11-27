plotPlate <- function(fileName) {
	require(ggplot2)
	if(!file.exists(fileName)) {
		stop(paste("file:",fileName,"does not exist"))
	}
	data <- read.csv(file=fileName,head=TRUE,stringsAsFactors=FALSE)
	ggplot(data,aes(x=as.numeric(substring(Well.positions,2)),y=substring(Well.positions,1,1))) +
		geom_tile(aes(fill=MeasAvg)) +
		scale_x_continuous("Column",breaks=1:12) +
		scale_y_discrete("Row",limits=rev(LETTERS[1:8])) +
		scale_fill_gradient(low="white",high="steelblue") +
		facet_grid(~Volume)
}
