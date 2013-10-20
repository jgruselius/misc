
plotPlate <- function(fileName) {
    require(ggplot2)
    if(!file.exists(fileName)) {
        stop(paste("file:",fileName,"does not exist"))
    }
    data <- read.csv(file=fileName,head=TRUE,stringsAsFactors=FALSE)

    ggplot(data[data$Volume==1,],aes(x=Column,y=Row)) +
        geom_tile(aes(fill=MeasAvg)) +
        scale_x_continuous(breaks=1:12) +
        scale_y_discrete(limits=rev(LETTERS[1:8])) +
        scale_fill_gradient(low="white",high="steelblue") +
        facet_grid(~Volume)
}