# Train Delay Estimation
This project is first of its kind, an attempt made to learn the delay trends of
Indian trains at their in-line stations. See doc dir for overview presentation;
papers (ITSC version accepted at [IEEE ITSC 2018](http://www.ieee-itsc2018.org) and
long version of Arxiv (https://arxiv.org/abs/1806.02825) and a tutorial on using
the code/ model/ data.

## Team
Ramashish Gaurav (2016 - ),
Himadri Mishra (2018 - ),
Biplav Srivastava, *main contact*.
For data or any other queries, email: my.better.rail@gmail.com

## Description
India runs the fourth largest railway transport network size carrying
over 8 billion passengers per year. However, the travel experience of
passengers is frequently marked by delays, i.e., late arrival of trains at
stations, causing inconvenience. In a first, we study the systemic delays
in train arrivals using norder Markov frameworks and experiment with two
regression based models. Using train running-status data collected for two
years, we report on an efficient algorithm for estimating delays at
railway stations with near accurate results. This work can help
railways to manage their resources, while also helping passengers
and businesses served by them to efficiently plan their activities.

## Tutorial to use our code
Please visit [tutorial](
https://github.com/R-Gaurav/train-delay-estimation/blob/master/doc/Tutorial.md)
to find the steps for using our code and setting up the experiment locally on
your system.

## Future work (how you can contribute to it...)
There are many avenues for extending current work. Please feel free to
contact us for any help.

- [Scaling] Expand the existing database of 135 trains (819 stations) to India wide.
- [Improving] Improve the accuracy of existing prediction framework. Examples are
time series prediction, neural networks.
- [Improving] The current prediction framework is off-line in approach, i.e. it learns by
batch processing the accumulated data. A realistic prediction framework will be
on-line, i.e. so that it can  keep learning with delays and railway network dynamics
throughout its lifetime.

--------
Suggestions and contributions are welcome.

