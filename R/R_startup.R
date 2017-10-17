library(ggplot2)
# Hide legend:
noleg <- theme(legend.position="none")
# Hide x axis labels and title:
hidex <- theme(axis.text.x=element_blank(),axis.title.x=element_blank())
# Put bars on x axis:
lobar <- scale_y_continuous(expand=c(0,0)) 
ggbar <- geom_bar(stat="identity")

# Color palettes:
cbPalette <- c("#999999","#E69F00","#56B4E9","#009E73","#F0E442","#0072B2","#D55E00","#CC79A7")
jCols1 <- c("#0099CC","#FF6666","#FFCC00","#9999FF","#339966","#FF5252")
jCols2 <- c("#1E88E5","#FF5252","#00C853","#AB47BC","#FFAB00","#00B8D4","#F06292","#69F0AE","#9575CD","#EF6C00","#3F51B5","#C62828","#388E3C","#6A1B9A","#D84315")

# Custom theme for ggthemr:
require(ggthemr)
jPalette <- define_palette(
	swatch = c("#757575","#1E88E5","#FF5252","#00C853","#AB47BC","#FFAB00","#00B8D4","#F06292","#69F0AE","#9575CD","#EF6C00","#3F51B5","#C62828","#388E3C","#6A1B9A","#D84315"),
	gradient = c(lower = "#67B26F", upper = "#4ca2cd"),
	background = "#F5F7F8",
	text = c("#263238", "#455A64"),
	line = c("#546E7A", "#78909C"),
	gridline = "#DDe3E6" 
)

savePlot <- function(name,w=800,h=600,r=120) {
	folder <- "~/Documents/plottar"
	dev.copy(png,paste(folder,name,sep="/"),width=w,height=h,res=r)
	dev.off()
}
# Rotate x labels:
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
	ggplot(NULL, aes(x = fit$model[2], y = fit$model[1])) +
	#ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) +
		geom_point() +
		stat_smooth(method = "lm", fullrange=T) +
		labs(x = names(fit$model)[2], y = names(fit$model)[1],
			 subtitle = paste("Adj R2 = ",signif(summary(fit)$adj.r.squared,5),
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
	ggplot(NULL, aes(x = fit$model[2], y = fit$model[1])) +
	#ggplot(fit$model, aes_string(x = names(fit$model)[2], y = names(fit$model)[1])) +
		geom_point() +
		stat_smooth(method = "lm", fullrange=T, se=F, col=col,size=0.5) +
		annotate("text",x,y,label=lab,parse=T) +
		xlab(names(fit$model)[2]) +
		ylab(names(fit$model)[1])
}

pbpaste <- function() {
	return(read.table(pipe("pbpaste"),sep="\t",header=T))
}

cat("Custom configuration loaded...")
