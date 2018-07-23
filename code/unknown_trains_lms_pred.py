#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file predicts the journey wise late minutes for unknown trains.
#
#       The path to saved trained models which would be loaded and employed to
#       predict late mins must be specified in function
#       "get_predicted_late_mins_list()" in file: "utilities/tt_utils.py".
#
#       N-Order Markov Late Minutes Prediction Framework for Unknown Trains.
#
#       To run this file execute:
#       `python unknown_trains_lms_pred.py rfr 10
#       jrny_wise_unknown_trains_lms_1ps_labenc_wonps_wdts
#       rmse_of_jrny_wise_lms_pred_unknown_trains_1ps_wonps_wdts`
#
#       Where the string "rfr" stands for the model employed to predict late
#       minutes, here "rfr" implies: Random Forest Regressor model. Numeral 10
#       can be changed to desired number of Nearest Neighbors stations out of
#       which first Known Station is to be chosen.
#       "jrny_wise_unknown_trains_lms_1ps_labenc_wonps_wdts" is the directory
#       where predicted late minutes are to be store and
#       "rmse_of_jrny_wise_lms_pred_unknown_trains_1ps_wonps_wdts" is the
#       directory where RMSE of predicted late minutes are to be dumped.
#

import pandas as pd
import pickle
import sys

from sklearn.metrics import mean_squared_error

from utilities.tt_utils import TrainingTestUtils as TTU

def get_journey_wise_late_mins_of_unknown_trains(
    ttu, train_num, setting, nn, mdl, exp_lms_output_dir, exp_rmse_output_dir):
  """
  Finds the journey wise late minutes of unknown trains, ie. last 82 trains of
  all 135 trains whose data has been collected so far.

  The data of last 82 trains has NOT been used for training the station models.

  Args:
    ttu <TTU()>: An object of TrainingTestUtils
    train_num <string>: A five digit train number string eg. "12307"
    setting <string>: <"test">
    nn <int>: Number of nearest neighbors of unknown stations
    mdl <string>: <"rfr"> # For Random Forest Regressor Models
                  <"lmr"> # For Linear Model Regressor Models
  """
  pred_lms_df = [] # To capture the predicted late mins for each journey
  pred_lms_rmse = [] # Late Minutes RMSE for each journey
  columns = ["Stations", "ActualLateMins", "PredictedLateMins"]
  train_df = ttu._cdr.get_train_journey_df(train_num, setting)

  # Get all the source station rows of each journey in train_df
  source_rows = train_df[train_df.scharr=="Source"].index.tolist()

  for i in range(len(source_rows)):
    # Obtain the single journey data frame
    sj_df = ttu._tdfu._generate_single_journey_df(train_df, i, source_rows)
    sj_df = sj_df[["station_code", "distance", "month", "weekday", "latemin"]]

    # Obtain the current single journey station list
    stn_list_sj = sj_df["station_code"].tolist()
    actual_late_mins_sj = sj_df["latemin"]
    pred_late_mins_sj = [0] # Assuming 0 late mins for source station
    num_of_unknown_stns = 0
    # Uncomment the following lines in `if else` case accordingly as per value
    # of N in N-OMLMPF. If N is chosen to be 3, it implies we will consider only
    # 3-previous-station models of suitable stations to predict the late minutes.\
    # Here, the value of N is chosen 1, so other `else` part of code is
    # commented out. Uncomment to generate desired results for different N.
    for j in range(1, len(stn_list_sj)):
      try:
        stn = stn_list_sj[j]

        if j == 1: # valid for only 1 previous station
          stns_hvng_1ps_model = ttu._pdr.get_stations_having_nps_model_list(nps=1)
          if stn not in stns_hvng_1ps_model:
            num_of_unknown_stns += 1
            # Get nn nearest neighbors of station "stn"
            nn_stns = ttu.get_station_nearest_neighbors_list(stn, 1, nn)
            stn = nn_stns[0] # Choose the 1st nearest neighbor station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 1, stn, pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        elif j == 2: # valid for only 2 previous stations
          stns_hvng_2ps_model = ttu._pdr.get_stations_having_nps_model_list(nps=2)
          if stn not in stns_hvng_2ps_model:
            num_of_unknown_stns += 1
            # Get nn nearest neighbors of station "stn"
            # Get nn nearest neighbors of station "stn"
            nn_stns = ttu.get_station_nearest_neighbors_list(stn, 2, nn)
            stn = nn_stns[0] # Choose the 1st nearest neighbor station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 2, stn, pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        elif j == 3: # valid for only 3 previous stations
          stns_hvng_3ps_model = ttu._pdr.get_stations_having_nps_model_list(nps=3)
          if stn not in stns_hvng_3ps_model:
            num_of_unknown_stns += 1
            # Get nn nearest neighbors of station "stn"
            # Get nn nearest neighbors of station "stn"
            nn_stns = ttu.get_station_nearest_neighbors_list(stn, 3, nn)
            stn = nn_stns[0] # Choose the 1st nearest neighbor station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 3, stn, pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        elif j == 4: # valid for only 4 previous stations
          stns_hvng_4ps_model = ttu._pdr.get_stations_having_nps_model_list(nps=4)
          if stn not in stns_hvng_4ps_model:
            num_of_unknown_stns += 1
            # Get nn nearest neighbors of station "stn"
            # Get nn nearest neighbors of station "stn"
            nn_stns = ttu.get_station_nearest_neighbors_list(stn, 4, nn)
            stn = nn_stns[0] # Choose the 1st nearest neighbor station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 4, stn, pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        else: # rest stations in journey are valid for 5 previous stations
          stns_hvng_5ps_model = ttu._pdr.get_stations_having_nps_model_list(nps=5)
          if stn not in stns_hvng_5ps_model:
            num_of_unknown_stns += 1
            # Get nn nearest neighbors of station "stn"
            # Get nn nearest neighbors of station "stn"
            nn_stns = ttu.get_station_nearest_neighbors_list(stn, 5, nn)
            stn = nn_stns[0] # Choose the 1st nearest neighbor station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 5, stn, pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
      except Exception as e:
        pred_late_mins_sj.append(pred_late_mins_sj[j-1])

    # Construct the data frame of Station Code, Actual Late Mins and
    # Predicted Late Mins for each journey
    for ele in zip(zip(stn_list_sj, actual_late_mins_sj), pred_late_mins_sj):
      pred_lms_df.append([ele[0][0], ele[0][1], ele[1]])

    # Mark the end of current journey
    pred_lms_df.append(["JRNY END", "-------", "-------"])
    # Calculate the RMSE of each journey for a train
    rmse = mean_squared_error(actual_late_mins_sj, pred_late_mins_sj)**0.5
    # Store the Number of Unknown Stations and RMSE of each journey of a train
    pred_lms_rmse.append((num_of_unknown_stns, rmse))
    # Print the RMSE of each journey for the given train "train_num"
    print ("Train Number:", train_num,
        "Number of Unknown Stations: ", num_of_unknown_stns, "RMSE: ", rmse)

  pred_lms_df = pd.DataFrame(pred_lms_df, columns=columns)
  pred_lms_df.to_csv(ttu._cdr._cdpath+mdl+"_model_data/" + exp_lms_output_dir +
      "/Train_" + train_num + "_jw_lms.csv", index=False)
  pickle.dump(pred_lms_rmse, open(ttu._pdr._pdpath+mdl + "_model_pickle_data/" +
      exp_rmse_output_dir + "/Train_" + train_num + "_jw_rmse.p", "wb"))

if __name__ == "__main__":
  mdl = sys.argv[1] # Get the model <"rfr"|"lmr">
  nn = int(sys.argv[2]) # Get the number of nearest neighbors
  exp_lms_output_dir = sys.argv[3] # Create this directory to store predicted
                                   # late minutes in each experiments for
                                   # different  values of n in nps.
  exp_rmse_output_dir = sys.argv[4] # Create this directory to store the RMSE
                                    # for predicted late minutes in each
                                    # experiment for different values of n.
                                    # Make sure it stays aligned with
                                    # exp_lms_output_dir.
  ttu = TTU()
  trains83 = ttu._pdr.get_all_trains()[52:] # Choose the rest 83 Unknown Trains
  for train in trains83:
    get_journey_wise_late_mins_of_unknown_trains(
        ttu, train, "unknown_test", nn, mdl, exp_lms_output_dir,
        exp_rmse_output_dir)
