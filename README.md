# Train Delay Estimation
A first attempt to model the train delays across stations in India (as of 2018).
Paper accepted at [IEEE ITSC 2018](http://www.ieee-itsc2018.org).

## Description
This project is first of its kind, an attempt made to learn the delay trends of
Indian trains at their in-line stations. We collected Train Running Status data
(with format same as that shown in [NTES](
https://enquiry.indianrail.gov.in/mntes/))
for a period of two years from March 2016 to February 2018 for 135 trains that
pass through MGS (Mughalsarai Station, one of the top busiest stations in India).

After required preprocessin of the data, we found that delays at stations depend
on the month during which the journey is made, as well as the stations previous
to the current station (at which we sought the predicted delay). As part of
learning algorithms we used Random Forest Regressors and Ridge Regressors to
devise a zero shot competent, scalable, train agnostic, late minutes prediction
framework inspired from Markov Process. We name our prediction framework as
*N*-Order Markov Late Minutes Prediction Framework (*N*-OMLMPF).

The *N*-OMLMPF inputs a train number, its journey route information (i.e.
stations along its journey route, distance of stations from source etc. - for
exact information, please see our paper on [arxiv](
https://arxiv.org/abs/1806.02825))
, station at which the user wishes to known the expected delay and a date. It
outputs the expected delay at that particular station.

The above only presents the gist of our work, it is highly recommended to go
through our paper mentioned above.

The code is highly commented with function docstrings. Please let me know if you
need help understanding them or setting up the experiments. The best way to set
an experiment environment on your system is to download and install [Anaconda](
https://www.anaconda.com/download/).


## Future Works (How you can contribute to it...)
Since this project is first of its kind, a large number of avenues exist for
scaling it up and improving the existing prediction framework.

As of 2018:
- Expand the existing database of 135 trains (819 stations) to India wide.
- Improve the existing prediction framework's accuracy.
- The current prediction framework is off-line in approach, i.e. it learns by
  batch processing the accumulated data. A true prediction framework must be
  on-line, i.e. it should keep learning the delays and railway network dynamics
  throughout its life.
- You can even explore other approaches for late minutes prediction, for example,
  time series prediction etc.

### Note:
This project is spearheaded by [Dr. Biplav Srivastava](
https://researcher.watson.ibm.com/researcher/view.php?person=us-biplavs).
