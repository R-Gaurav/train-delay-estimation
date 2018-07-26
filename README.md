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

## Tutorial (How to use this code to train and test the models...)
We only share the raw data and not the pre-trained models. Each saved pre-trained
model is approximately 40MB or more, hence not feasible to share. However by
following simple steps you can easily train the prediction models and use it for
predicting delays at railway stations.

The tutorial below details the steps to train Random Forest Regressor models (the
most effective ones compared to Ridge Regressor models).

To set up an experimental environment, follow the below steps in precisely the
same order as mentioned. The preferred environment is Linux.

### Setting up the directory
1> Clone this repo on your local system by executing below command.\
`git clone https://github.com/R-Gaurav/train-delay-estimation-ITSC2018.git`

2> Prepare **data** directory and **models** directory.\
  a) Change the directory: `cd train-delay-estimation-ITSC2018`\
  b) Untar the data folder **Train_Delay_Estimation_Data_March_2016_February_2018.tar** by executing below command:\
    `tar -zxf Train_Delay_Estimation_Data_March_2016_February_2018.tar`\
  c) Rename **Train_Delay_Estimation_Data_March_2016_February_2018** to **data**.\
     Execute: `mv Train_Delay_Estimation_Data_March_2016_February_2018 data`\
  d) Create a new directory named **models** where your trained Random Forest Models would be saved.\
     Execute: `mkdir models`\
  c) Before you proceed further, make sure you have following contents under **train-delay-estimation-ITSC2018** directory:\
    README.md\
    Train_Delay_Estimation_Data_March_2016_February_2018.tar (you can remove it).\
    code\
    data\
    misc\
    models

### Setting up the environment variables in file **env.py**
1> Navigate to directory **train-delay-estimation-ITSC2018/code/utilities**.

2> Open **env.py**.

3> Set the `project_dir_path` variable to the location where you have downloaded **train-delay-estimation-ITSC2018** directory.

4> Change no more variables.

### Creating pickle data
1> Move to **data** directory.

2> Execute: `mkdir pickle_data && cd pickle_data`.

3> Create list of
### Create training data (Table 3 in paper) to train the models
1> Move to the **code** directory.

2>
