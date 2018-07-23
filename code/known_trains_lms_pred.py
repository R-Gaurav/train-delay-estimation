#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file predicts the journey late minutes of known trains (52 trains).
#       Prints the RMSE of each journey.
#
#       The path to saved trained models which would be loaded and employed to
#       predict late mins must be specified in function
#       "get_predicted_late_mins_list()" in file: "utilities/tt_utils.py".
#
#       N-Order Markov Late Minutes Prediction Framework for Known Trains.
#
#       To run this file execute:
#
#       `python known_trains_lms_pred.py rfr jrny_wise_known_trains_lms_1ps_labenc
#       rmse_of_jrny_wise_lms_pred_known_trains_1ps`
#
#       to run Random Forest Regressor Station models to predict late minutes
#       and store the late mins prediction in
#       "rny_wise_known_trains_lms_1ps_labenc" directory and corresponding RMSEs
#       in "rmse_of_jrny_wise_lms_pred_known_trains_1ps" directory.
#
#       IMPORTANT NOTE: Make sure to remove the unwanted columns in data frame
#                       depending on experiments. This can be done in function:
#                       "remove_unwanted_columns_df()" defined in
#                       "utilities/tt_utils.py", which gets eventually called in
#                       "get_predicted_late_mins_at_station_float()".
#
#

import pickle
import pandas as pd
import sys

from sklearn.metrics import mean_squared_error

from utilities.tt_utils import TrainingTestUtils as TTU

def get_journey_wise_late_mins_of_known_trains(
    ttu, train_num, setting, mdl, exp_lms_output_dir, exp_rmse_output_dir):
  """
  Finds the journey wise late minutes of Known Trains, ie. first 52 trains of
  all 135 trains whose data has been collected so far.

  The data of first 52 train has been used for training the station models.

  Args:
    ttu <TTU()>: An object of TrainingTestUtils
    train_num <string>: A five digit train numebr string eg. "12307"
    setting <string>: <"traininig"|"cross_validation"|"known_test">
    mdl <string>: <"rfr"|"lmr">
                "rfr": Random Forest Regressor Models
                "lmr": Linear Model Regressor Models
    exp_lms_output_dir <string>: <"jrny_wise_known_trains_lms_1ps_labenc" | ..>
                                 Desired output directory of predicted latemins.
                                 Change this directory with values of n in nps.
    exp_rmse_output_dir <string>: <"rmse_of_jrny_wise_lms_pred_known_trains_1ps"
                                   |..>
                                 Desired output directory of predicted latemins
                                 RMSEs. Changes this directory with values of n
                                 in nps. Make sure it stays aligned with
                                 exp_lms_output_dir.

  """
  pred_lms_df = [] # To caputre predicted late mins for each journey
  pred_lms_rmse = [] # Late Minutes RMSE for each journey
  columns = ["Stations", "ActualLateMins", "PredictedLateMins"]
  train_df = ttu._cdr.get_train_journey_df(train_num, setting)

  # Get all the source station rows of each journey in train_df
  source_rows = train_df[train_df.scharr=="Source"].index.tolist()

  for i in range(len(source_rows)):
    # Obtain the single journey dataframe
    sj_df = ttu._tdfu._generate_single_journey_df(train_df, i, source_rows)
    sj_df = sj_df[["station_code", "distance", "month", "weekday", "latemin"]]

    # Obtain the current single journey station list
    stn_list_sj = sj_df["station_code"].tolist()
    actual_late_mins_sj = sj_df["latemin"]
    pred_late_mins_sj = [0] # Assuming 0 late mins for source station

    # Uncomment the following lines in `if else` case accordingly as per value
    # of N in N-OMLMPF. If N is chosen to be 3, it implies we will consider only
    # 3-previous-station models of suitable stations to predict the late minutes.
    # Here, the value of N is chosen 1, so other `else` part of code is
    # commented out. Uncomment to generate desired results for different N.
    #
    # Depending on the Experiment you choose, make sure to remove the unwanted
    # columns in the call of function "get_predicted_late_mins_at_station_float".

    for j in range(1, len(stn_list_sj)):
      try: # Try to predict the late minutes for this station in single journey.
        if j == 1: # valid for only 1 previous station
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 1, stn_list_sj[j], pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        else: # j == 2: # valid for only 2 previous stations
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 2, stn_list_sj[j], pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        """
        elif j == 3: # valid for only 3 previous stations
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 3, stn_list_sj[j], pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        elif j == 4: # valid for only 4 previous stations
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 4, stn_list_sj[j], pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        else: # rest stations in journey are valid for 5 previous stations
          plm = ttu.get_predicted_late_mins_at_station_float(train_num, sj_df,
              j+source_rows[i], 5, stn_list_sj[j], pred_late_mins_sj, j, mdl)
          pred_late_mins_sj.append(plm)
        """
      # Case when a new station comes whose trained model does not exist
      except KeyError:
        # KeyError is obtained while creating row data frame for a station but
        # the previous station is not be present in station to index dict. Hence
        # set the late minutes at the current station as that of previous one.
        pred_late_mins_sj.append(pred_late_mins_sj[j-1])
      except Exception as e:
        # Set the late minutes at that station for which no trained model exist
        # as the late minutes at the immediate previou station.
        pred_late_mins_sj.append(pred_late_mins_sj[j-1])

    # Construct the data frame of Station Code, Actual Late Mins and
    # Predicted Late Mins for each journey
    for ele in zip(zip(stn_list_sj, actual_late_mins_sj), pred_late_mins_sj):
      pred_lms_df.append([ele[0][0], ele[0][1], ele[1]])

    # Mark the end of current journey
    pred_lms_df.append(["JRNY END", "-------", "-------"])
    # Store the RMSE of each journey for a train
    rmse = mean_squared_error(actual_late_mins_sj, pred_late_mins_sj)**0.5
    pred_lms_rmse.append(rmse)
    # Print the RMSE of each journey for the given train "train_num"
    print "Train Number:", train_num, "RMSE:", rmse

  pred_lms_df = pd.DataFrame(pred_lms_df, columns=columns)
  pred_lms_df.to_csv(ttu._cdr._cdpath+mdl+"_model_data/" + exp_lms_output_dir +
      "/Train_" + train_num + "_jw_lms.csv", index=False)
  pickle.dump(pred_lms_rmse, open(ttu._pdr._pdpath+mdl+"_model_pickle_data/" +
      exp_rmse_output_dir + "/Train_" + train_num + "_jw_rmse.p", "wb"))


if __name__ == "__main__":
  mdl = sys.argv[1] # Accept <"rfr"|"lmr">
  exp_lms_output_dir = sys.argv[2] # Create this directory to store predicted
                                   # late minutes in each experiments for
                                   # different  values of n in nps.

  exp_rmse_output_dir = sys.argv[3] # Create this directory to store the RMSE
                                    # for predicted late minutes in each
                                    # experiment for different values of n.
                                    # Make sure it stays aligned with
                                    # exp_lms_output_dir.
  ttu = TTU()
  trains52 = ttu._pdr.get_all_trains()[:52] # Choose the first 52 trains, which
                                            # are Known Trains.
  for train in trains52:
    get_journey_wise_late_mins_of_known_trains(
        ttu, train, "known_test", mdl, exp_lms_output_dir,
        exp_rmse_output_dir)
