#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file creates data for training and evaluating the different models.
#
#       To create training data to train models, make sure that the running
#       status data of trains are in "data/trains_training_file" and similarly
#       for test data of trains.
#
#       Output station wise data frames are stored in
#       "data/52tr_stations_training_data/<n>ps_training_data/" depending on the
#       value of n.
#
#       To run this file execute following command (for both the functions).
#
#       python create_training_data.py training 3
#
#       It creates data frames of "training" setting for a current station with
#       3 previous stations.
#
#       This file also has a function to generate the known 596 stations
#       features data frame.
#       Station Features DF: ["Station", "latitude", "longitude",
#                             "traffic_strength", "degree_strength"]
#
#       To run a specific function, uncomment it in __main__ section.
#

import sys
import pandas as pd
import pickle

from joblib import Parallel, delayed

from utilities.df_utils import TrainDataFrameUtils as TDFU

def generate_known_current_station_df(
    tdfu, current_station, setting="complete_training", n=3):
  """
  Returns a data frame of the current station. The data frame consists of n
  previous station features to the current station. The setting if set to
  "cross_validation", generates data frames similar to "training" from Known
  Trains only to evaluate the models, not to cross-validate the late minutes
  prediction algorithm.

  Args:
    tdfu <TDFU()>: An object of TrainDataFrameUtils
    current_station <string>: A known station name which should be one among
                              the stations of 52 trains. eg. "CNB"
    setting <string>: <"training"|"cross_validation"|"complete_training">
    n <int>: Number of previous stations to the current station preferred
             <1|2|3|4|5>, default value is 3
  """
  station_df = []
  column_names_list = tdfu._get_column_names_list(n)
  trains = tdfu._pdr.get_all_trains()
  trains52 = trains[:52] # Choose the first 52 trains which are Known Trains
                         # Rest 83 trains in list are Unknown Trains.

  # Iterate over all trains.
  # Get the complete df of each train.
  # Get the single journey df out of a complete df of each train.
  # For each single journey df find the station which is the current station
  # and append the n previous stations info to the station_df.
  for train_num in trains52:
    train_df = tdfu._cdr.get_train_journey_df(train_num, setting)

    # Get all the source station rows of each journey
    source_rows = train_df[train_df.scharr=="Source"].index.tolist()
    for i in range(len(source_rows)):
      sj_df = tdfu._generate_single_journey_df(train_df, i, source_rows)

      # Choose the required columns
      sj_df = sj_df[["station_code", "distance",
                     "month", "weekday", "latemin"]]
      station_list = sj_df["station_code"].tolist() # Obtain the station list

      # Check if the sj_df is wrong due to extended journey
      if station_list != sj_df.station_code.unique().tolist():
        print "Repeated stations found, Wrong DF, Check Train: ", train_num
        print "Obtained stations: ", station_list
        print "Actual stations: ", sj_df.station_code.unique().tolist()
        return
      else:
        for j in range(n+source_rows[i], len(station_list)+source_rows[i]):
          station = station_list[j-source_rows[i]]
          if station == current_station:
            # train_type. zone. is_superfast, month, weekday
            feature_list = [tdfu._generate_train_type_str(train_num),
                 tdfu._generate_zone_str(train_num),
                 tdfu._is_superfast_str(train_num),
                 tdfu._generate_month_str(sj_df, j),
                 tdfu._generate_weekday_str(sj_df, j)]
            # n_prev_station
            feature_list.extend(
                tdfu._generate_n_prev_station_codes_list(sj_df, j, n))
            # n_ps_late_mins
            feature_list.extend(
                tdfu._generate_n_prev_stn_late_mins_list(sj_df, j, n))
            # dist_bwn_stn_n-1_n
            feature_list.extend(
                tdfu._generate_n_prev_dist_bwn_stn_list(sj_df, j, n))
            # stn_n_dist_frm_src
            feature_list.extend(
                tdfu._generate_n_prev_stn_dist_from_source_list(sj_df, j, n))
            # tfc_of_stn_n
            feature_list.extend(
                tdfu._generate_n_prev_stn_tfc_strength_list(sj_df, j, n))
            # deg_of_stn_n
            feature_list.extend(
                tdfu._generate_n_prev_stn_deg_strength_list(sj_df, j, n))
            # crnt_stn_tfc, set n = 0
            feature_list.extend(
                tdfu._generate_n_prev_stn_tfc_strength_list(sj_df, j, 0))
            # crnt_stn_deg, set n = 0
            feature_list.extend(
                tdfu._generate_n_prev_stn_deg_strength_list(sj_df, j, 0))
            # crnt_stn_dist_frm_src, set n = 0
            feature_list.extend(
                tdfu._generate_n_prev_stn_dist_from_source_list(sj_df, j, 0))
            # crnt_stn_late_mins, set n = 0
            feature_list.extend(
                tdfu._generate_n_prev_stn_late_mins_list(sj_df, j, 0))

            station_df.append(feature_list)

  station_df = pd.DataFrame(station_df, columns = column_names_list)
  station_df.to_csv((tdfu._cdr._cdpath + "52tr_stations_" + setting+"_data/" +
                     str(n) + "ps_" + setting + "_data/Station_" +
                     current_station + ".csv"), index=False)
  print "Station: ", current_station, " Done!"
  return station_df

def generate_known_stations_features_df(pdr):
  """
  This function generates known stations features data frame helpful in
  projecting unknown stations to known stations.

  Args:
    pdr <PDR()>: A Pickle Data Reader object
  """
  known_stations = pdr.get_all_52trains_stations()
  stn_ftrs_df = []
  columns = ["Station", "Latitude", "Longitude", "Degree_Strength",
      "Traffic_Strength"]
  geo_crdnates = pdr.get_station_coordinates_dict()
  deg_strength = pdr.get_station_degree_strength_dict()
  tfc_strength = pdr.get_station_traffic_strength_dict()
  for stn in known_stations:
    stn_ftrs_df.append([stn, geo_crdnates[stn][0], geo_crdnates[stn][1],
                        deg_strength[stn], tfc_strength[stn]])
  stn_ftrs_df = pd.DataFrame(stn_ftrs_df, columns=columns)
  pickle.dump(stn_ftrs_df,
      open(pdr._pdpath + "known_596_stations_features_df.p", "wb"))

if __name__ == '__main__':
  setting = sys.argv[1]
  n = int(sys.argv[2])
  tdfu = TDFU()
  pdr = tdfu._pdr
  stns_of_52trains = pdr.get_all_52trains_stations() # Get all Known Stations.
################################################################################
  # To create training or cross-validation data, runs parallely on 4 processors.
  Parallel(n_jobs=16)(delayed(generate_known_current_station_df)(tdfu, stn,
      setting, n) for stn in stns_of_52trains)
################################################################################
  # To create stations' features data frame.
  # generate_known_stations_features_df(pdr)
################################################################################
