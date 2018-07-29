#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file creates all the required pickle data (used throughout the code
#       as pre-computed data) taking reference from the existing data on github
#       repo. Make sure you have create "pickle_data" folder under "data"
#       directory.
#

import numpy as np
import pandas as pd
import pickle

from utilities.df_utils import TrainDataFrameUtils as TDFU

class CreatePickleData(object):
  def __init__(self):
    self._tdfu = TDFU()
    self._pdr = self._tdfu._pdr
    self._cdr = self._tdfu._cdr

  def create_52trains_unique_stations_pickle(self):
    """
    Creates a list of unique stations covered by all 52 "training" trains.
    It considers the complete journey of known trains (March 2016 to Feb 2018).
    """
    trains52 = self._pdr.get_all_trains()[:52] # First 52 are Known Trains.
    tr52_unique_stations = []
    for train in trains52:
      df = self._cdr.get_train_complete_journey_df(train)
      stations = df["station_code"]
      tr_unique_stations = np.unique(stations)
      tr52_unique_stations.extend(tr_unique_stations)

    tr52_unique_stations = np.unique(tr52_unique_stations).tolist()
    pickle.dump(tr52_unique_stations,
                open(self._pdr._pdpath+"52trains_unique_stations.p", "wb"))
    print ("52 Known Trains Unique Stations pickle data dumped in pickle_data"
           " directory. Number of unique stations: %s"
           % len(tr52_unique_stations))
    print "-" * 80

  def create_135trains_unique_stations_pickle(self):
    """
    Creates a list of unique stations covered by all 135 trains (Known + Unknown
    trains). It considers the complete journey of trains (March 2016 to Feb 2018).
    """
    trains135 = self._pdr.get_all_trains()
    tr135_unique_stations = []
    for train in trains135:
      df = self._cdr.get_train_complete_journey_df(train)
      stations = df["station_code"]
      tr_unique_stations = np.unique(stations)
      tr135_unique_stations.extend(tr_unique_stations)

    tr135_unique_stations = np.unique(tr135_unique_stations).tolist()
    pickle.dump(tr135_unique_stations,
                open(self._pdr._pdpath+"135trains_unique_stations.p", "wb"))
    print ("135 Trains Unique Stations pickle data dumped in pickle_data"
           " directory. Number of unique stations: %s"
           % len(tr135_unique_stations))
    print "-" * 80

if __name__ == "__main__":
  ob = CreatePickleData()
  ob.create_52trains_unique_stations_pickle()
  ob.create_135trains_unique_stations_pickle()
