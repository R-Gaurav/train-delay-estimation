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
To get the data, please contact Dr. Srivastava at biplavs@us.ibm.com.

After required preprocessing of the data, we found that delays at stations depend
on the month during which the journey is made, as well as the stations previous
to the current station (at which we sought the predicted delay). As part of
learning algorithms we used Random Forest Regressors and Ridge Regressors to
devise a Zero Shot competent, scalable and train agnostic, late minutes prediction
framework inspired from Markov Process. We name our prediction framework as
*N*-Order Markov Late Minutes Prediction Framework (*N*-OMLMPF).

The *N*-OMLMPF inputs a train number, its journey route information (i.e.
stations along its journey route, distance of stations from source etc. - for
more information, please see our paper on [arxiv](
https://arxiv.org/abs/1806.02825)) and station at which the user wishes to known
the expected delay and a date. It then outputs the expected delay at that particular
station.

The above only presents the gist of our work, it is highly recommended to go
through our paper mentioned above, before proceeding ahead.

The code is highly commented with function docstrings. Please let me know if you
need help understanding them or setting up the experiments. The best way to set
an experiment environment on your system is to download and install [Anaconda](
https://www.anaconda.com/download/).


## Future work (how you can contribute to it...)
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

## Tutorial (how to use this code to train and test the models...)
Upon contacted we share the raw data but not the pre-trained models. Each
saved pre-trained model is approximately 40MB or more, hence not feasible to
share all of them. However with the help of following simple steps you can easily
train the prediction models and use it for predicting delays at railway stations.

The tutorial below details the steps to train Random Forest Regressor models (the
most effective ones compared to Ridge Regressor models) on n-prev-stns training
data-frames of Known Stations, with station codes removed from them (refer
Experiments and Result Analysis section in our paper - Exp 3, Exp 4).

To set up an experimental environment, follow the below steps precisely in the
same order as mentioned. The preferred environment is Linux.

### Setting up the directory structure.
1> Clone this repo on your local system by executing below command.\
`git clone https://github.com/R-Gaurav/train-delay-estimation.git`

2> Change the directory: `cd train-delay-estimation` and execute:
`./metadata_setup.sh` from inside `train-delay-estimation` direcotry.

### Setting up the environment variables in file **env.py**
1> Navigate to directory **train-delay-estimation/code/utilities**.

2> Open **env.py**.

3> Set the `project_dir_path` variable to the location where you have downloaded
the **train-delay-estimation** directory.

4> Save **env.py**.

### Creating pickle data
1> I have already provided some data in pickle format which were either manually
created or collected from internet via REST APIs. Although you need to create
few more data in pickle format.

To do this, just execute `python create_pickle_data.py`.

### Creating the training data (Table III in paper) to train the models
1> Move to the **code** directory.

2> Execute: `python code/create_training_data.py training 1` to create training
data for 1 previous station data-frame, similarly replace `1` with <`2`,`3`,`4`,`5`> for
creating data with respect to that many number of previous stations.

On a system with 4 logical cores (you can get the number of logical cores on
you system by executing `htop` or `top` (followed by pressing `1` key)), it
takes nearly 7 hours to prepare 1-prev-stn data frames. For 2-prev-stn data
frames it takes 9 hours, so expect it to keep increasing for higher number
of previous station data frames.

NOTE: The data frames are created parallely, computation is done on all cores.

For more information, go through the description mentioned in file:
`create_training_data.py`.

### Training the regression models
1> Move to **code** directory.

2> Execute `python rfr_stn_models_training_file.py 1` to train 1-prev-stn Random
Forest Regressor (RFR) models. Similary change `1` to <`2`,`3`,`4`,`5`>
to train other models. However you would be required to prepare training data for
them first though.

   On executing the above command, you will see a continuous output on command
   prompt:

           .
           .
           .
           .
   CAR 6.60625167783
   CBH 1.71117789831
   CBJ 17.4222160169
   CCK 3.79114575446
   CD 3.31220839301
   CDMR 5.39912244203
   CGR 8.08489734899
   CH 10.4774022913
   CHL 5.99947173966
   CHTI 67.8594204912
   CKDL 12.6303575828
   CKTD 5.57649677578
   CLG 4.48826310353
   CNB 62.4855739456
           .
           .
           .
           .

   where "CAR", CBH" are station codes and floating numbers beside them are
   RMSEs which evaluate the fit of models on training data itself.

   On a system with 4 logical cores it takes nearly an hour to train 1-prev-stn
   RFR models, for other n-prev-stn models it takes nearly the same time.

### Predicting delays of train's test data
1> Move to **code** directory.

2> Execute `python known_trains_lms_pred.py rfr 2`.
The output on shell is similar to below:


                         .
                         .
                         .
                         .
      Train Number: 12307 RMSE: 39.7547311759
      Train Number: 12307 RMSE: 27.7902472271
      Train Number: 12307 RMSE: 69.2035611394
      Train Number: 12307 RMSE: 90.8565136872
      Train Number: 12307 RMSE: 56.4806884838
      Train Number: 12307 RMSE: 50.1364333031
      Train Number: 12307 RMSE: 34.8328977349
      Train Number: 12307 RMSE: 16.3028024387
      Train Number: 12307 RMSE: 24.3166122244
      Train Number: 12307 RMSE: 26.6479429784
      Train Number: 12307 RMSE: 67.5090362829
      Train Number: 12307 RMSE: 29.016842432
      Train Number: 12307 RMSE: 23.8403707468
                         .
                         .
                         .
                         .

where each row corresponds to one journey of a train and the corresponding RMSE
obtained on the test data for that journey.

For Unknown Trains late minutes prediction, execute:
`python unknown_trains_lms_pred.py rfr 10 2`

This command will predict late minutes for unknown trains by using RFR
models and will consider 10 Nearest Neighbors for a station. It will
consider 2 previous stations i.e. n = 2 in n-OMLMPF.

Suggestions and contributions are always welcome.
