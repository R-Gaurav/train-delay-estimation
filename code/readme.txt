This Train Delay Estimation project aims to find a pattern in delays at stations
during journey of trains in India. A set of 135 trains is considered, out of
which 52 trains journey data are used for training various prediction models and
it is tested on another set of 83 trains. Prediction of near accurate late
minutes proves the existence of a pattern and our successful attempt to do so.

For more information on algorithm, data collection and data division please
refer the paper.

Here, description of files in this repository is given.

/data:
  > Contains the information of data collected from March 2016 to June 2017 for
  135 trains.

/models:
  > Contains the trained models for each stations, which form the basis of our
  late minutes prediction framework.

/readers:
  > Contains the helper code to read data from csv files and pickle files.

/utilities:
  > Contains the helper code to generate data frames and to build our train-test
  algorithm.

/result_analysis.py:
  > Code to analyse the results.

/create_training_data.py:
  > Code to create training data i.e. a Training Data Frame for each Known
  Station from each Known Train.

/cross_validation_file.py:
  > Code to evaluate the trained models.

/rfr_stn_models_training_file.py:
  > Code to train Random Forest Regressors on Training Data Frame.

/known_trains_lms_pred.py:
  > Implementation of N-Order Late Minutes Prediction Framework for Known Trains.

/unknown_trains_lms_pred.py:
  > Implementation of N-Order Late Minutes Prediction Framework for UnKnown
  Trains.

One can train the various n-previous-station models of Random Forest, Linear
Regressors and Neural Network Rgressors by executing the corresponding files as
metioned above. The total size of saved models exceed 120 GB, with at-least 40GB
for each setting of Random Forests Models. In case you need the pre-trained
models contact me.
