#!/bin/bash

# This script sets up the directory structure for executing the code.

echo "######################################"
echo "#                                    #"
echo "#       TRAIN DELAY ESTIMATION       #"
echo "#                                    #"
echo "######################################"

echo "Setting up the metadata (directory structure)..."
yes '' | sed 5q # Echo 5 blank lines.

# Untaring the tar data file.
echo "Untaring data... Train_Delay_Estimation_Data_March_2016_February_2018.tar"
tar -zxf Train_Delay_Estimation_Data_March_2016_February_2018.tar
echo "Untaring done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

echo "Renaming 'Train_Delay_Estimation_Data_March_2016_February_2018' to 'data'"
mv Train_Delay_Estimation_Data_March_2016_February_2018 data
echo "Renaming done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

# Setting up the directory structure where trainig data would be saved.
echo "Creating a new directory '52tr_stations_training_data' inside 'data'"
echo "directory where Known Station's n-previous station training data-frames"
echo "would be saved, which would be later used to train Random Forest Regressor"
echo "models."
mkdir data/52tr_stations_training_data

echo "Creating subdirectories inside '52tr_stations_training_data', where"
echo "Known Station's respective n-previous-station data-frames will be saved."
for n in {1..5}
do
  echo "Creating '"$n"ps_training_data' to store $n-previous station data-frames."
  mkdir data/52tr_stations_training_data/"$n"ps_training_data
  echo "-----------------------------------------------------------------------"
done
echo "Setting up the directory structure for saving training data done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

# Setting up the directory structure where trained models would be saved.
echo "Creating a new directory 'models' where your trained Random Forest"
echo "Regressor (RFR) models would be saved."
mkdir models
mkdir models/rfr_models
for n in {1..5}
do
  echo "Creating '"$n"ps_rfr_labenc_models' to store the RFR models trained"
  echo "from $n-previous station training data-frames."
  mkdir models/rfr_models/"$n"ps_rfr_labenc_models
  echo "-----------------------------------------------------------------------"
done
echo "Setting up the directory structure for saving RFR trained models done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

# Setting up the directory structure for saving predicted late minutes and
# correspoding RMSEs of test journey data.
echo "Creating a subdirectory 'rfr_model_data' inside 'data' directory to save"
echo "the predicted late minutes of test journey data."
mkdir data/rfr_model_data
for n in {1..5}
do
  echo "Creating 'jrny_wise_known_trains_lms_"$n"ps_labenc' to store journey"
  echo "wise predicted late-minutes of Known Train's test data with "$n"-OMLMPF."
  mkdir data/rfr_model_data/jrny_wise_known_trains_lms_"$n"ps_labenc
  echo "-----------------------------------------------------------------------"
  echo "Creating 'jrny_wise_unknown_trains_lms_"$n"ps_labenc' to store journey"
  echo "wise predicted late-minutes of Unknown Train's test data with "$n"-OMLMPF."
  mkdir data/rfr_model_data/jrny_wise_unknown_trains_lms_"$n"ps_labenc
  echo "-----------------------------------------------------------------------"
done
echo "Setting up the directory structure for saving predicted late-minutes done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

echo "Creating a subdirectory 'rfr_model_pickle_data' inside 'data/pickle_data'"
echo "to save RMSEs of predicted late-minutes in pickle format."
mkdir data/pickle_data/rfr_model_pickle_data
for n in {1..5}
do
  echo "Creating 'rmse_of_jrny_wise_lms_pred_known_trains_"$n"ps' to store RMSE"
  echo "of journey wise predicted late minutes from "$n"-OMLMPF algorithm for"
  echo "Known Trains in pickle format."
  mkdir data/pickle_data/rfr_model_pickle_data/rmse_of_jrny_wise_lms_pred_known_trains_"$n"ps
  echo "-----------------------------------------------------------------------"
  echo "Creating 'rmse_of_jrny_wise_lms_pred_unknown_trains_"$n"ps' to store RMSE"
  echo "of journey wise predicted late minutes from "$n"-OMLMPF algorithm for"
  echo "Unknown Trains in pickle format."
  mkdir data/pickle_data/rfr_model_pickle_data/rmse_of_jrny_wise_lms_pred_unknown_trains_"$n"ps
  echo "-----------------------------------------------------------------------"
done
echo "Setting up the directory structure for saving RMSEs in pickle format done!"
echo "*************************************************************************"
yes '' | sed 5q # Echo 5 blank lines.

echo "#########################################################################"
echo "#      You are all setup to run the codes as per your convenience.      #"
echo "#  It is advised to go through the above output messages to understand  #"
echo "#                   the overall directory structure.                    #"
echo "#########################################################################"
