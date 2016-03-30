library(ggplot2)

t12307 <- read.csv('Train12307.csv')

# Exploring the relation between latemin and distance/stations. However there can be a numerical relation between distance and
# latemins, also, on the other hand we can get some latent info about delays at train stations (need to be brainstormed)

aggregate(latemin~distance,t12307,mean) 
#aggregate(latemin~station_code,t12307,mean)
#aggregate(t12307$latemin,by=list(dist=t12307$distance),mean) In place of mean, we can pass functions : sd, max, var, median

#plot the latemin with distance
stn <- t12307[c(1:26),3]
delay <- aggregate(latemin~distance,t,mean)
delay$station <- stn

# Saving a plot in the working directory
jpeg('Latemin Vs Distance.jpg')
plot(delay$distance,delay$latemin,type="l")
lines(delay$distance,delay$latemin,col="red")
dev.off()

# Set a linear model on data
lin_reg <- lm(latemin ~ distance+station_code,data=t12307)
summary(lin_reg) # Has R-Squared : 0.7676 (without station_code: 0.6499, so station_code is required)
# We can also include more variables in formula : difference between combination of scharr and schdep with actarr and actdep
# schdep-scharr = total scheduled stop time at stations and so on...


