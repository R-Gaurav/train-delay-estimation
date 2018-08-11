#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# Desc: This file reads the csv data.
#

import numpy as np
import pandas as pd

class CSVDataReader(object):

  def __init__(self, data_path=""):
    self._cdpath = data_path

  def get_train_journey_df(self, train_num, setting="training"):
    """
    Returns the data frame of the given train. The data frame corresponds to
    either training or test setting.

    Args:
      train_num <string>: Train number eg. "12307" whose data frame is required
      setting <string>: <"training"|"cross_validation"|"known_test"|
                        "unknown_test">
    """
    tr_grp = ("52_known_" if (setting == "training" or setting == "known_test"
              or setting == "cross_validation") else "83_unknown_")
    train_df = pd.read_csv(
        (self._cdpath+tr_grp+"trains_"+setting+"_folder/Train"+train_num+".csv"))
    return train_df

  def get_n_prev_station_csv_df(self, station, setting, n):
    """
    Returns the n previous station training data frame of given station

    Args:
      station <string>: should be one among 52trains unique stations
      setting <string>: <"training"|"cross_validation">
      n <int>: <1|2|3|4|5>
    """
    stn_csv = pd.read_csv(
        (self._cdpath+"52tr_stations_"+setting+"_data/"+str(n)+
        "ps_"+setting+"_data/Station_"+station+".csv"))
    return stn_csv

  def get_jw_pred_late_mins_of_train_df(self, train_num, nps=4, rfr_mdl="",
      group="known"):
    """
    Returns the data frame of Actual Late Mins and Predicted Late Mins for a
    train's cross validation data.

    Args:
      train_num <string>: Train number eg. "12307" whose predicted late mins df
                          is required.
      group <string>: <"known"|"unknown">
      nps <int>: number of previous stations considered for prediction.
      rfr_mdl <string>: <""|"_wonps_wdts"|"_without_nps_codes">
    """
    df = pd.read_csv(self._cdpath+"rfr_model_data/"+"jrny_wise_"+group+"_trains"
        +"_lms_"+str(nps)+"ps"+"_labenc"+rfr_mdl+"/"+"Train_"+
        train_num+"_jw_lms.csv")
    return df

  def get_train_complete_journey_df(self, train_num):
    """
    Returns a complete data frame of collected data for a train.

    Args:
      train_num <string>: Train number eg. "12307" whose complete journey df is
                          required.
    """
    df = pd.read_csv(self._cdpath+
        "csv_Mar16_Feb18_all_trains_135_months_weekdays/Train"+train_num+".csv")
    return df
