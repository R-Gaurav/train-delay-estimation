#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file provides the basic utility functions for training and testing
#       the models.
#

from env import * # Import it first as it imports data_path and models_path.
import joblib
import numpy as np
import pandas as pd
import pickle

from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors as NN

from df_utils import TrainDataFrameUtils as TDFU
from readers.pickle_data_reader import PickleDataReader as PDR
from readers.csv_data_reader import CSVDataReader as CDR


class TrainingTestUtils(object):

  def __init__(self):
    self._tdfu = TDFU()
    self._pdr = PDR(data_path)
    self._cdr = CDR(data_path)
    self._model_path = models_path
    self._stn_geo_crdnates = self._pdr.get_station_coordinates_dict()
    self._stn_deg_strength = self._pdr.get_station_degree_strength_dict()
    self._stn_tfc_strength = self._pdr.get_station_traffic_strength_dict()

  def _get_labenc_of_cat_var_df(self, df, cat_var, cat_var_dict):
    """
    Returns the station data frame where the "cat_var" column is the label
    encoding of the categorial variables in passed station data frame "df"

    Args:
      df <pandas.DataFrame>: The data frame whose categorical variables are to
                             be encoded.
      cat_var <string>: The column name of the categorical variables to be
                        encoded eg. "train_type".
      cat_var_dict <dict{}>: A python dictionary to provide label encodings for
                             categorical variables.
    """
    l = []
    cat_var_clmn = df[cat_var]
    for ele in cat_var_clmn:
      l.append(cat_var_dict[ele])
    l = pd.DataFrame(l, columns=[cat_var])
    temp = df.pop(cat_var)
    df = pd.concat([l, df], axis=1)
    return df

  def _get_labenc_station_df(self, df, n):
    """
    Returns the complete training data frame of a station where all its
    categorical variables are encoded.

    Args:
      df <pandas.DataFrame>: The data frame whose categorical variables are to
                             be label encoded.
      n <int>: The n in "n previous stations" data frame.
    """
    # Encode Train Type
    train_type_dict = self._pdr.get_labenc_train_type_dict()
    df = self._get_labenc_of_cat_var_df(df, "train_type", train_type_dict)

    # Encode zone
    zone_dict = self._pdr.get_labenc_zone_dict()
    df = self._get_labenc_of_cat_var_df(df, "zone", zone_dict)

    # Encode month
    month_dict = self._pdr.get_labenc_month_dict()
    df = self._get_labenc_of_cat_var_df(df, "month", month_dict)

    # Encode weekday
    weekday_dict = self._pdr.get_labenc_weekday_dict()
    df = self._get_labenc_of_cat_var_df(df, "weekday", weekday_dict)

    # Encode n previous stations
    station_dict = self._pdr.get_labenc_station_dict()
    for i in range(n):
      df = self._get_labenc_of_cat_var_df(
          df, str(i+1)+"_prev_station", station_dict)

    return df

  def generate_row_df(self, train_num, sj_df, j, n):
    """
    Returns a single row data frame info to test the late minutes prediction
    algorithm.

    Args:
      train_num <string>: A five digit train number eg. "12307".
      sj_df <pandas.DataFrame>: A single journey data frame from which row data
                                frame is to be obtained.
      j <int>: The row index of the current station in sj_df whose n previous
               stations' info is required.
      n <int>: Number of previous stations.
    """
    column_names_list = self._tdfu._get_column_names_list(n)

    # train_type. zone. is_superfast, month, weekday
    feature_list = [self._tdfu._generate_train_type_str(train_num),
         self._tdfu._generate_zone_str(train_num),
         self._tdfu._is_superfast_str(train_num),
         self._tdfu._generate_month_str(sj_df, j),
         self._tdfu._generate_weekday_str(sj_df, j)]
    # n_prev_station
    feature_list.extend(
        self._tdfu._generate_n_prev_station_codes_list(sj_df, j, n))
    # n_ps_late_mins
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_late_mins_list(sj_df, j, n))
    # dist_bwn_stn_n-1_n
    feature_list.extend(
        self._tdfu._generate_n_prev_dist_bwn_stn_list(sj_df, j, n))
    # stn_n_dist_frm_src
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_dist_from_source_list(sj_df, j, n))
    # tfc_of_stn_n
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_tfc_strength_list(sj_df, j, n))
    # deg_of_stn_n
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_deg_strength_list(sj_df, j, n))
    # crnt_stn_tfc
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_tfc_strength_list(sj_df, j, 0))
    # crnt_stn_deg
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_deg_strength_list(sj_df, j, 0))
    # crnt_stn_dist_frm_src
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_dist_from_source_list(sj_df, j, 0))
    # crnt_stn_late_mins
    feature_list.extend(
        self._tdfu._generate_n_prev_stn_late_mins_list(sj_df, j, 0))

    feature_list_df = pd.DataFrame([feature_list], columns=column_names_list)
    # Obtain the label encoded feature_list_df
    feature_list_df = self._get_labenc_station_df(feature_list_df, n)
    return feature_list_df

  def remove_unwanted_columns_df(self, df, n):
    """
    Returns the passed data frame after removal of unwanted columns from it.

    Args:
      df <pandas.DataFrame>: The data frame from which columns are to be removed.
      n <int>: Number of previous stations to the current station.
    """
    # Remove "stn_n_dist_frm_src"
    # Remove "tfc_of_stn_n"
    # Remove "deg_of_stn_n"
    # Remove "n_prev_station"
    for k in range(n):
      #temp = df.pop("stn_"+str(k+1)+"_dist_frm_src")
      #temp = df.pop("tfc_of_stn_"+str(k+1))
      #temp = df.pop("deg_of_stn_"+str(k+1))
      temp = df.pop(str(k+1)+"_prev_station")
    return df

  def get_predicted_late_mins_list(self, current_station, n, df, mdl):
    """
    Returns the predicted late mins at the current_station.

    Args:
      current_station <string>: Station Code for the station in question
                                eg. "CNB", used to choose the RFR model.
      n <int>: Number of previous station to the current_station to choose the
               RFR model.
      df <pandas.DataFrame>: The data frame of current_station to predict late
                             minutes at it.
      mdl <string>: <"rfr"|"lmr"|"nnr">
                    "rfr": Random Forest Regressor Models.
                    "lmr": Linear Model Regressor Models (not reliable).
                    "nnr": Neural Network Regressor Models (not converged).
    """
    model = joblib.load(self._model_path + mdl + "_models/" + str(n) +
        "ps_" + mdl + "_labenc_models_complete_wonps_wdts/" + current_station +
        "_label_encoding_model.sav")
    pred_late_mins = model.predict(df)
    return pred_late_mins

  def _get_selected_stations_df(self, stn_index_list, df):
    """
    Returns a station features data frame of selected stations.

    Args:
      stn_index_list <list>: A list of stations indices for which station
                             features data frame is to be constructed.
      df <pandas.DataFrame>: A Complete DataFrame of 596 known station features
    """
    selected_station_df = df.iloc[stn_index_list]
    return selected_station_df

  def get_station_nearest_neighbors_list(self, station, nps, n):
    """
    Returns the n nearest neighbors stations to given station among the stations
    in passed data frame "df".

    Args:
      station <string>: The station code for which nearest neighbors are needed.
      nps <int>: Number of previous stations to choose stations having nps model.
      n <int>: Number of nearest neighbors needed.
    """
    # Choose the stations who have the respective nps models.
    # If the unknown station occurs as 3rd station in the complete journey, then
    # the nearest known station should have a 3 previous station model and so on.
    stns_hvng_nps_mdls = self._pdr.get_stations_having_nps_model_list(nps)

    # Get the station features data frame for known stations having nps models
    df = self._pdr.get_known_596_stations_features_df()
    df = df[df.Station.isin(stns_hvng_nps_mdls)]

    query_stn_feature = [[self._stn_geo_crdnates[station][0],
                         self._stn_geo_crdnates[station][1],
                         self._stn_deg_strength[station],
                         self._stn_tfc_strength[station]]]
    # First choose neighbors which are geographically closer
    lat_lon_df = df[["Latitude", "Longitude"]]

    lat_lon_query_stn_ftr = [[self._stn_geo_crdnates[station][0],
                              self._stn_geo_crdnates[station][1]]]
    ll_nbrs = NN(n_neighbors=n, algorithm="auto").fit(lat_lon_df)
    # ll_indices are directly indexed corresponding to stns_hvng_nps_mdls
    ll_distances, ll_indices = ll_nbrs.kneighbors(lat_lon_query_stn_ftr)

    # Subselect the chosen stations features from the complete station
    # features df.
    selected_station_fts_df = self._get_selected_stations_df(ll_indices[0], df)

    # Then choose neighbors based on degree and traffic strength among the
    # above chosen geographically closer stations.
    deg_tfc_df = selected_station_fts_df[["Degree_Strength", "Traffic_Strength"]]
    deg_tfc_query_stn_ftr = [[self._stn_deg_strength[station],
                              self._stn_tfc_strength[station]]]
    dt_nbrs = NN(n_neighbors=n, algorithm="auto").fit(deg_tfc_df)
    # dt_indices are indexed with 0, so not directly related to
    # stns_hvng_nps_mdls
    dt_distances, dt_indices = dt_nbrs.kneighbors(deg_tfc_query_stn_ftr)

    # Once the dt_indices are obtained where the stations are arranged as per
    # increasing distance of degree and traffic strength features, get the
    # station codes from the df at those indices (since the dt_indices are
    # indexed from 0 onwards with respect to the ll_indices, hence the following
    # code). Also the ll_indices are with respect to the df.
    final_nearest_neighbors_stns_list = [df.iloc[ll_indices[0][idx]].Station
        for idx in dt_indices[0]]
    return final_nearest_neighbors_stns_list

  def get_predicted_late_mins_at_station_float(self, train_num, sj_df, idxof_stn,
      n, station, pred_lms_sj, j, mdl):
    """
    Returns the predicted late minutes at given "station".

    Args:
      train_num <string>: A five digit train number eg. "12307".
      sj_df <pandas.DataFrame>: A single journey data frame.
      idxof_stn <int>: Index of current station in single journey data frame.
      n <int>: N in number of previous station.
      station <string>: Station Code at which late mins are to be predicted.
      pred_lms_sj <list>: Predicted Late Minutes list.
      j <int>: The current station index in station list of sj_df.
      mdl <string>: <"rfr"> # For random forest regressor model.
    """
    row_df_nps = self.generate_row_df(train_num, sj_df, idxof_stn, n)
    temp = row_df_nps.pop("crnt_stn_late_mins")
    # Remove unwanted columns from the row data frame
    row_df_nps = self.remove_unwanted_columns_df(row_df_nps, n)

    # Set the late minutes at n previous stations as predicted ones
    for i in range(n):
      row_df_nps[str(i+1)+"_ps_late_mins"] = pred_lms_sj[j-(i+1)]

    plm = self.get_predicted_late_mins_list(station, n, row_df_nps, mdl)
    return plm[0]

  def replace_unknown_stations_with_known_stations_df(self, train_df, n):
    """
    Returns a data frame with unknown stations replaced by known stations
    depending on the value of n for the nth nearest neighbor.

    Args:
      train_df <python.DataFrame>: A train data frame of all journeys.
      n <int>: n for nearest neighbor <1..10>.
    """
    nn_station_codes = []
    known_stations = self._pdr.get_all_52trains_stations()
    station_codes = train_df["station_code"]
    for station in station_codes:
      if station not in known_stations:
        # Get 10 nearest neighbors of unknown stations (hard coded)
        nn_stations = self.get_station_nearest_neighbors_list(station, 10)
        nn_station_codes.append(nn_stations[n-1])
      else:
        nn_station_codes.append(station)
    train_df["station_code"] = nn_station_codes
    return train_df
