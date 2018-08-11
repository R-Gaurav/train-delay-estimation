#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# Desc: This file reads the pickle data.
#

import pickle
import numpy as np


class PickleDataReader(object):

  def __init__(self, data_path=""):
    self._pdpath = data_path+"pickle_data/"

  def get_all_trains(self):
    """
    Returns a list of all 135 trains' train numbers.
    First 52 trains in list are Known Trains. Next 83 trains are Unknown Trains.
    """
    all_trains = pickle.load(open(self._pdpath+"all_trains135.p", "rb"))
    return all_trains

  def get_all_52trains_stations(self):
    """
    Returns a list of all 596 Known Stations of Known Trains.
    """
    stations_52trains = pickle.load(
        open(self._pdpath+"52trains_unique_stations.p", "rb"))
    return stations_52trains

  def get_all_135trains_stations(self):
    """
    Returns a list of all 799 Known Stations + Uknown Stations of all Known
    Trains and Unknown Trains.
    """
    stations_135trains = pickle.load(
        open(self._pdpath+"135trains_unique_stations.p", "rb"))
    return stations_135trains

  def get_labenc_train_type_dict(self):
    """
    Returns a dictionary of train type (key) vs numeric label (value).
    """
    train_type_dict = pickle.load(
        open(self._pdpath+
        "label_encodings/all_train_types_label_encoding_dict.p", "rb"))
    return train_type_dict

  def get_labenc_zone_dict(self):
    """
    Returns a dictionary of zone (key) vs numeric label (value).
    """
    zone_dict = pickle.load(
        open(self._pdpath+
        "label_encodings/all_zones_label_encoding_dict.p", "rb"))
    return zone_dict

  def get_labenc_month_dict(self):
    """
    Returns a dictionary of month (key) vs numeric label (value).
    """
    month_dict = pickle.load(
        open(self._pdpath+
        "label_encodings/all_months_label_encoding_dict.p", "rb"))
    return month_dict

  def get_labenc_weekday_dict(self):
    """
    Returns a dictionary of weekday (key) vs numeric label (value).
    """
    weekday_dict = pickle.load(
        open(self._pdpath+
        "label_encodings/all_weekdays_label_encoding_dict.p", "rb"))
    return weekday_dict

  def get_labenc_station_dict(self):
    """
    Returns a dict of station (key) vs numeric label (value).
    It is supposed to be universal set of all 4359 stations in India, for which
    numeric labels are assigned randomly.
    """
    station_dict = pickle.load(
        open(self._pdpath+
        "label_encodings/all_stations_label_encoding_dict.p", "rb"))
    return station_dict

  def get_station_degree_strength_dict(self):
    """
    Returns a dictionary of station (key) vs degree strength (value).
    This dictionary contains info about only 799 Known and Unknown Stations.
    """
    stn_deg_strength = pickle.load(
        open(self._pdpath+"station_degree_strength_dict.p", "rb"))
    return stn_deg_strength

  def get_station_traffic_strength_dict(self):
    """
    Returns a dictionary of station (key) vs traffic strength (value).
    This dictionary contains info about only 799 Known and Unknown Stations.
    """
    stn_tfc_strength = pickle.load(
        open(self._pdpath+"station_traffic_strength_dict.p", "rb"))
    return stn_tfc_strength

  def get_station_coordinates_dict(self):
    """
    Returns a dictionary of station (key) vs a tuple of latitude and longitude
    of station (value).
    This dictionary contains info about only 799 Known and Unknown Stations.
    """
    stn_coordinate = pickle.load(
        open(self._pdpath+"station_to_lat_lng_dict.p", "rb"))
    return stn_coordinate

  def get_known_596_stations_features_df(self):
    """
    Returns a pandas DataFrame of station features of all 596 Known Stations.
    Valid Known Stations depending on their presence in `stations_having_nps_
    models.p` would be chosen from here to perform kNN on them to find a nearest
    Known Station for an Unkown Station.
    """
    stn_ftrs_df = pickle.load(
        open(self._pdpath+"known_596_stations_features_df.p", "rb"))
    return stn_ftrs_df

  def get_stations_having_nps_model_list(self, nps):
    """
    Returns a list of stations which have an n_previous_station model.
    Args:
      nps <int>: n in n_previous_stations models
    """
    stns_hvng_nps_mdls = pickle.load(
        open(self._pdpath+"stations_having_"+str(nps)+"ps_models.p", "rb"))
    return stns_hvng_nps_mdls

  def get_rmse_of_journey_wise_lms_pred_list(self, n, group, train, rfr_mdl=""):
    """
    Returns a list of RMSEs of different journeys undertaken by a train in
    given group and rfr_mdl with N-OMLMPF (depending on the value of n).

    Args:
      n <int>: <1|2|3|4|5>
      group <string>: <"known"|"unknown">
      rfr_mdl <string>: <""|"_wonps_wdts">
      train <string>: A five digit train number eg. "12307"
    """
    rmse_list = pickle.load(
        open(self._pdpath+"rfr_model_pickle_data/rmse_of_jrny_wise_lms_pred"+
        "_"+group+"_trains_"+str(n)+"ps"+rfr_mdl+"/Train_"+train+"_jw_rmse.p",
        "rb"))
    return rmse_list

  def get_all_trains_inline_stations_dict(self):
    """
    Returns a dict of key as train number and values as a list of stations
    inline in its journey.
    """
    train_stns_dict = pickle.load(
        open(self._pdpath+"trains_inline_stations_dict.p", "rb"))
    return train_stns_dict
