par(bg="white",cex=0.8)

par(mar=c(1,4,1,0))
par(fig=c(0,0.25,0,1))
plot(a1$qpcr_mol,ylim=c(0,11),ylab="qPCR conc. (nM)",xlab="",xaxt="n")

par(mar=c(1,0,1,0))
par(fig=c(0.25,0.3,0,1),new=TRUE)
boxplot(a1$qpcr_mol,ylim=c(0,11),axes=FALSE)

par(mar=c(1,4,1,0))
par(fig=c(0.35,0.6,0,1),new=TRUE)
plot(a1$miseq_reads1,ylim=c(0,1.8e6),ylab="Reads",xlab="",xaxt="n")

par(mar=c(1,0,1,0))
par(fig=c(0.6,0.65,0,1),new=TRUE)
boxplot(a1$miseq_reads1,ylim=c(0,1.8e6),axes=FALSE)

par(mar=c(1,4,1,0))
par(fig=c(0.7,0.95,0,1),new=TRUE)
plot(a1$miseq_reads2,ylim=c(0,1.8e6),ylab="Reads",xlab="",xaxt="n")

par(mar=c(1,0,1,0))
par(fig=c(0.95,1,0,1),new=TRUE)
boxplot(a1$miseq_reads2,ylim=c(0,1.8e6),axes=FALSE)