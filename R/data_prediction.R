data_pred <- function(data) {
	require("calibrate")
	df <- data[!is.na(data$hiseq_pct1),]

	f <- function(y0,pct,output,lanes) { y0+pct/1E2*output*0:lanes }

	plot(NULL,ylim=c(0,650),xlim=c(1,36),xlab="Lanes",ylab="M reads")
	#plot(NULL,ylim=c(250,350),xlim=c(34,36),xlab="Lanes",ylab="M reads")
	cols <- rainbow(nrow(df))
	grid()

	N = 23
	yield = 200
	t1 = 214.5
	t2 = 429

	for(i in 1:nrow(df)) {
		v <- df$hiseq_pct1[i]
		lines(1:N,f(v*yield/1E2,v,yield,N-1),col=cols[i],lty=2)
		v <- df$reads_23_observed[i]
		lines(c(0,N),c(0,v),col=cols[i],lty=1)
	}

	pred <- df$hiseq_pct1*yield*N/1E2
	final <- (yield*(36-N)+sum(pred))*df$targeted_pct/1E2
	pool <- (final-pred)/(36-N)/yield*1E2

	for(i in 1:nrow(df)) {
		v <- df$hiseq_pct1[i]
		lines(N:36,f(v*N/1E2*yield,pool[i],yield,36-N),col=cols[i],lty=2)
		v <- df$reads_23_observed[i]
		v2 <- df$reads_23_observed[i] + df$reads_13_prelim[i]
		lines(c(N,36),c(v,v2),col=cols[i],lty=1)
	}

	abline(h=t1,lty=2,col="darkgreen")
	abline(h=t2,lty=2,col="blue")
	abline(v=N,lty=3,lwd=1.2,col="red")

	textxy(1,t1,t1,cx=0.8,dcol="darkgreen")
	textxy(1,t2,t2,cx=0.8,dcol="blue")
	textxy(N,0,N,cx=0.8,dcol="red")
}