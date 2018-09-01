# Tutorial: Using Train Delay Estimation

## Background
We collected Train Running Status data (with format same as that shown in [NTES](
https://enquiry.indianrail.gov.in/mntes/)) for a period of two years from March 2016
to February 2018 for 135 trains that pass through MGS (Mughalsarai Station, one of the
top busiest stations in India). After required preprocessing of the data, we
found that delays at stations depend on the month during which the journey is made,
as well as the stations previous to the current station (at which we
sought the predicted delay). As part of learning algorithms we
used Random Forest Regressors and Ridge Regressors to
devise a Zero Shot competent, scalable and train agnostic, late minutes prediction
framework inspired from Markov Process. We name our prediction framework as
*N*-Order Markov Late Minutes Prediction Framework (*N*-OMLMPF).

The *N*-OMLMPF inputs a train number, its journey route information (i.e.
stations along its journey route, distance of stations from source etc. - for
more information, please see our papers in doc directory) and station at
which the user wishes to known the expected delay and a date. It then
outputs the expected delay at that particular station.

The above only presents the gist of our work, it is highly recommended to go
through our paper mentioned above, before proceeding ahead.

The code is highly commented with function docstrings. Please let us know if you
need help understanding them or setting up the experiments. The best way to set
an experiment environment on your system is to download and install [Anaconda](
https://www.anaconda.com/download/).

### List of trains covered so far
['12307', '12331', '12801', '12802', '12815', '12816', '12875', '12876', '13010', '13050', '13119', '13131', '13133', '13151', '13238', '13483', '14055', '18612', '22911', '12178', '12318', '12327', '12354', '12361', '12362', '12372', '12395', '12569', '12818', '12942', '14003', '15632', '15635', '15636', '22811', '22812', '22824', '12305', '12326', '12424', '12444', '12578', '12937', '22409', '09012', '09305', '12149', '12282', '12333', '12335', '12382', '13239', '01660', '02050', '02265', '02397', '03209', '03210', '03291', '03563', '03564', '04039', '04040', '04401', '04405', '04406', '04821', '05066', '06032', '12141', '12150', '12175', '12295', '12296', '12301', '12302', '12304', '12308', '12309', '12312', '12313', '12317', '12319', '12320', '12322', '12325', '12328', '12332', '12334', '12356', '12369', '12381', '12392', '12397', '12398', '12401', '12423', '12439', '12454', '12495', '12496', '12506', '12741', '12817', '12826', '12947', '12948', '12987', '12988', '13005', '13006', '13008', '13009', '13049', '13202', '13240', '13255', '13307', '13308', '13414', '15022', '15483', '15645', '15668', '18103', '18104', '18311', '18609', '18631', '19313', '22308', '22405', '22406', '22488', '25631']

## How to Use Code and Other Artifacts
Upon contacted, we will share the raw data but not the pre-trained models. Each
saved pre-trained model is approximately 40MB or more, hence not feasible to
share all of them. However with the help of following simple steps, one can easily
train the prediction models and use it for predicting delays at railway stations.

The tutorial below details the steps to train Random Forest Regressor models (the
most effective ones compared to Ridge Regressor models) on n-prev-stns training
data-frames of Known Stations, with station codes removed from them (refer
Experiments and Result Analysis section in our paper - Exp 3, Exp 4).

To set up an experimental environment, follow the below steps precisely in the
same order as mentioned. The preferred environment is Linux.

**Note**: The code works with Python 2.7

### Setting up the directory structure.
1> Clone this repo on your local system by executing below command.\
`git clone https://github.com/R-Gaurav/train-delay-estimation.git`

2> After you download the tar file of data:
`Train_Delay_Estimation_Data_March_2016_February_2018.tar`, move it inside the
`train-delay-estimation` directory. You can download this data by contacting us
at my.better.rail@gmail.com.

3> From inside `train-delay-estimation` directory execute:
`./metadata_setup.sh` to setup the required directory structure along 
with automatically installing the dependencies in **requirements.txt**.

### Setting up the environment variables in file **env.py**
1> Navigate to directory **train-delay-estimation/code/utilities**.

2> Open **env.py**.

3> Set the `project_dir_path` variable to the location where you have downloaded
the **train-delay-estimation** directory.

4> Save **env.py**.

### Creating pickle data
1> Move to the **code** directory.

2> We have already provided some data in pickle format which were either manually
created or collected from internet via REST APIs. Although you need to create
few more data in pickle format.

To do this, just execute `python create_pickle_data.py`.

### Creating the training data (Table III in paper) to train the models
1> Move to the **code** directory.

2> Execute: `python create_training_data.py training 1` to create training
data for 1 previous station data-frame, similarly replace `1` with <`2`,`3`,`4`,`5`> for
creating data with respect to that many number of previous stations.

On a system with 4 logical i5 cores (you can get the number of logical cores on
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

2> Execute `python known_trains_lms_pred.py rfr 1`.
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
`python unknown_trains_lms_pred.py rfr 10 1`

This command will predict late minutes for unknown trains by using RFR
models and will consider 10 Nearest Neighbors for a station. It will
consider 2 previous stations i.e. n = 2 in n-OMLMPF.

### Deploying the Train Delay Estimation Service on your local machine
Make sure that you have all the trained Random Forest Regressors models up to N=
5.

1> Move to **tde_service** directory.

2> In `env.py` file, set the `project_dir_path` to the location where you have
downloaded the `train_delay_estimation` directory.

3> Execute: `python app.py`. The flask server would be running by default on
loopback address: 127.0.0.1 at port 5000.

From other terminal:

4> Execute: `curl http://127.0.0.1:5000/12307` to get the predicted late minutes
at all the in-line stations of train 12307 on current date.

5> Execute: `curl http://127.0.0.1:5000/12307/2018-07-23` to get predicted late
minutes at all the in-line stations of train 12307 on date 23rd July 2018.

6> Execute `curl http://127.0.0.1:5000/12307/ALD/today` to get predicted late
minutes of train 12307 at station ALD (Allahabad) on current date.

7> Execute `curl http://127.0.0.1:5000/12307/ALD/2018-12-09` to get predicted
late minutes for train 12307 at station ALD on 9th Dec 2018.

The logs can be obtained in `train-delay-estimation/tde_service/logs/tde_logs.log`
file.

----------

