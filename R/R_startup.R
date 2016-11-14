library(ggplot2)
noleg <- theme(legend.position="none")
ggbar <- geom_bar(stat="identity")
cbPalette <- c("#999999","#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7")
jColors <- c("#0099CC")

savePlot <- function(name,w=800,h=600,r=120) {
	folder <- "~/Documents/plottar"
	dev.copy(png,paste(folder,name,sep="/"),width=w,height=h,res=r)
	dev.off()
}

rtext <- function(a=90,hj=1,vj=0.5) {
	return(theme(axis.text.x=element_text(angle=a,hjust=hj,vjust=vj)))
}

import <- function(filePath) {
	nas <- c("NaN","NA","N/A","#N/A","-","--")
	data <- read.delim(filePath,na.strings=nas)
	if(length(data) < 2) data <- read.csv(filePath,na.strings=nas)
	if(length(data) < 2) stop(paste("Seems data is neither tab- or comma-separated"))
	return(data)
}

ggplotRegression <- function(fit) {
	require(ggplot2)
	ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) +
		geom_point() +
		stat_smooth(method = "lm", fullrange=T) +
		labs(title = paste("Adj R2 = ",signif(summary(fit)$adj.r.squared,5),
			"Intercept =",signif(fit$coef[[1]],5),
			" Slope =",signif(fit$coef[[2]],5),
			" P =",signif(summary(fit)$coef[2,4],5)))
}

# This is prettier:
ggplotRegression2 <- function(fit,yadj=0.5,xadj=0.5,col="lightblue") {
	require(ggplot2)
	yrange <- max(fit$model[,1]) - min(fit$model[,1])
	xrange <- max(fit$model[,2]) - min(fit$model[,2])
	y <- min(fit$model[,1]) + yrange*yadj
	x <- min(fit$model[,2]) + xrange*xadj
	lab <- as.character(as.expression(paste("italic(r)^2==",signif(summary(fit)$r.squared,5))))
	ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) +
		geom_point() +
		stat_smooth(method = "lm", fullrange=T, se=F, col=col,size=0.5) +
		annotate("text",x,y,label=lab,parse=T) +
		theme_bw()
}

cat("Custom configuration loaded...")
