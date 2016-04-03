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

### 3rd April ############################################################################################

time_sarr <- strptime(x=as.character(t12307$scharr), format="%H:%M")
time_aarr <- strptime(x=as.character(t12307$actarr), format="%H:%M")

time_delay <- (time_aarr-time_sarr)/60 (Divide by 60 to convert from seconds to minutes) 
# This is same as "latemin"
# However we want to do get total delay minutes up to station in query, and not the delay minutes at that station, i.e. each row
# will have delay minutes upto one station before, for example, for stations A, B, C, and D, B will have delay minutes the train
# got up to station A, for station C -> up to station B, for station D -> up to station C.

time_delay <- t12307$latemin
time_delay <- time_delay[seq(1,length(time_delay)-1)] # Shift time delay by one station ahead
# prepend 0 to time_delay now...
time_delay <- c(0,time_delay)
# Now for every instance of journey in data, the time_delay at the source station be 0,
no_of_stations <- length(t12307$station_code)
time_delay[seq(1,length(time_delay),no_of_stations)] <- 0 # Set 0 time_delay at each source station
time_delay[time_delay < 0] <- 0 # Remove negative values from time_delay column
t12307$time_delay<- time_delay # Add the column time_delay to data frame

# Fit a linear model
lin_reg <- lm(latemin ~ distance+station_code+time_delay, data=t12307)
summary(lin_reg)
# RSquared Error : 0.9834, Outstanding model, but it was expected, as "latemin" can have linear relation with "time_delay"
# and was evident in summary of model, since the slope came out to be 1.02 and statistical importance of "distance" vanished.
# In real environment we would not have time_delay up to a query station, so we can compute time_delay on mean of delays
# ("latemin") so far and fit a linear model on it








