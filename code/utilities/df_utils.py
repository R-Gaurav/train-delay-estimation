#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# Desc: Provides necessary utilities helpful for DataFrame creation
#

# Import it first, as it imports data_path and models_path and paths to other
# modules namely pickle_data_reader and csv_data_reader.
from env import *

import pickle
import pandas as pd

from pickle_data_reader import PickleDataReader as PDR
from csv_data_reader import CSVDataReader as CDR

class TrainDataFrameUtils(object):

  def __init__(self):
    """
    Initializes a list which contains train type <"EXPRESS"|..>, is superfast
    <True|False> and zone <"CR"|"ECR"..> information.

    Args:
      train_num <string>: A five digit train number e.g. "12307"
    """
    self._pdr = PDR(data_path)
    self._cdr = CDR(data_path)

  def _generate_train_type_str(self, train_num):
    """
    Generates the train type <"SPECIAL"|"EXPRESS"|"OTHER"> based on the first
    digit of the train number.

    Args:
      train_num <string>: A five digit train number e.g. "12307"
    """
    if (train_num[0]=='0'):
      return "SPECIAL"
    if (train_num[0]=='1' or train_num[0]=='2'):
      return "EXPRESS"
    return "OTHER"

  def _get_train_type_col_name_list(self):
    return ["train_type"]

  def _is_superfast_str(self, train_num):
    """
		Returns boolean <True|False> depending on the second digit of the train
		number.

    Args:
    	train_num <string>: A five digit train number e.g. "12307"
    """
    if train_num[1]=='2':
      return True
    return False

  def _get_is_superfast_col_name_list(self):
    return ["is_superfast"]

  def _generate_zone_str(self, train_num):
    """
    Returns zone string <"JS"|"CR"|...> based on the second and third digit of
    the train number.

    Args:
    	train_num <string>: A five digit train number e.g. "12307"
  	"""
    if train_num[1]=='2':
      if train_num[2]=='0':
      	return "JS" # 20 is for Shatabdis and Jan Shatabdis on all zonal railways
      if train_num[2]=='1':
        return "CR" # 21 is for superfasts on CR and WCR (formerly only CR)
      if train_num[2]=='2':
        return "NR" # 22 is for superfasts from various zones -
										# NR, NCR, NWR (formerly only NR).
      if train_num[2]=='3':
        return "ER" # 23 is for superfast on ER and ECR
      if train_num[2]=='4':
        return "NR" # 24 is for superfast on NR, NCR and NWR (formerly only NR)
      if train_num[2]=='5':
        return "NER" # 25 is for superfast on NER and NFR
      if train_num[2]=='6':
        return "SR" # 26 is for superfast on SR and SWR (formerly only SR)
      if train_num[2]=='7':
        return "SCR" # 27 is for superfast on SCR and SWR (formerly only SCR)
      if train_num[2]=='8':
        return "SER" # 28 is for superfast on SER, SECR and ECoR
										 # (formerly only SER)
      if train_num[2]=='9':
        return "WR" # 29 is for superfast on WR, WCR and NWR (formerly only WR)
      return "OTHER"

    if train_num[1]=='0':
      return "KR" # 0 is for Konkan Railway
    if train_num[1]=='1':
      return "CR" # 1 is for CR, WCR and NCR(?)
    if train_num[1]=='3':
      return "ER" # 3 is shared by ER and ECR
    if train_num[1]=='4':
      return "NR" # 4 is for NR, NCR and NWR
    if train_num[1]=='5':
      return "NER" # 5 is shared by NER and NFR
    if train_num[1]=='6':
      return "SR" # 6 is for SR and SWR
    if train_num[1]=='7':
      return "SCR" # 7 is shared by SCR and SWR
    if train_num[1]=='8':
      return "SER" # 8 is for SER and ECoR
    if train_num[1]=='9':
      return "WR" # 9 is for WR, NWR and WCR
    return "OTHER"

  def _get_zone_col_name_list(self):
    return ["zone"]

  def _generate_month_str(self, sj_df, j):
    """
    Returns the month value in the single journey data frame a particula row j.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame corresponding to one
                                single journey.
      j <int>: The row index in sj_df at which month info is required.
    """
    return sj_df["month"][j]

  def _get_month_col_name_list(self):
    return ["month"]

  def _generate_weekday_str(self, sj_df, j):
    """
    Returns the weekday value in the single journey data frame a particula row j.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame corresponding to one
                                single journey.
      j <int>: The row index in sj_df at which weekday info is required.
    """
    return sj_df["weekday"][j]

  def _get_weekday_col_name_list(self):
    return ["weekday"]

  def _generate_n_prev_station_codes_list(self, sj_df, j, n):
    """
    Returns a list containing n previous station codes to the current station.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               stations codes list is required.
      n <int>: Number of previous stations.
    """
    l = []
    for i in range(n):
      l.append(sj_df["station_code"][j-(i+1)])
    return l

  def _get_n_prev_stations_col_names_list(self, n):
    """
    Returns a list ["1_prev_station", "2_prev_station" ...] upto value of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [(str(i+1)+"_prev_station") for i in range(n)]


  def _generate_n_prev_stn_late_mins_list(self, sj_df, j, n):
    """
    Returns a list containing n previous station's late minutes.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               late minutes list is required.
      n <int>: Number of previous stations.
    """
    l = []
    # If current station (i.e. n == 0)
    if n == 0:
      l.append(sj_df["latemin"][j])
      return l

    for i in range(n):
      l.append(sj_df["latemin"][j-(i+1)])
    return l

  def _get_n_prev_stn_late_mins_col_names_list(self, n):
    """
    Returns a list ["1_ps_late_mins", "2_ps_late_mins" ...] upto value of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [(str(i+1)+"_ps_late_mins") for i in range(n)]

  def _get_crnt_stn_late_mins_col_names_list(self):
    return ["crnt_stn_late_mins"]

  def _generate_n_prev_dist_bwn_stn_list(self, sj_df, j, n):
    """
    Returns a list containing n previous station's inter distance between them.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               distance between stations list is required.
      n <int>: Number of previous stations.
    """
    l = []
    for i in range(n):
      l.append(sj_df["distance"][j-i] - sj_df["distance"][j-(i+1)])
    return l

  def _get_n_prev_dist_bwn_stn_col_names_list(self, n):
    """
    Returns a list ["dist_bwn_stn_0_1", "dist_bwn_stn_1_2" ...] upto value of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [("dist_bwn_stn_"+str(i)+"_"+str(i+1)) for i in range(n)]

  def _generate_n_prev_stn_deg_strength_list(self, sj_df, j, n):
    """
    Returns a list containing n previous stations degree strength to the
    current station.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               stations' degree strength list is required.
      n <int>: Number of previous stations.
    """
    l = []
    # If current station (i.e. n == 0)
    if n == 0:
      l.append(
          self._pdr.get_station_degree_strength_dict()[
          sj_df["station_code"][j]])
      return l

    for i in range(n):
      l.append(
          self._pdr.get_station_degree_strength_dict()[
          sj_df["station_code"][j-(i+1)]])
    return l

  def _get_n_prev_stn_deg_col_names_list(self, n):
    """
    Returns a list ["deg_of_stn_1", "deg_of_stn_2" ...] upto value of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [("deg_of_stn_"+str(i+1)) for i in range(n)]

  def _get_crnt_stn_deg_col_names_list(self):
    return ["crnt_stn_deg"]

  def _generate_n_prev_stn_tfc_strength_list(self, sj_df, j, n):
    """
    Returns a list containing n previous stations traffic strength to the
    current station.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               stations' traffic strength list is required.
      n <int>: Number of previous stations.
    """
    l = []
    # If current station (i.e. n == 0)
    if n == 0:
      l.append(
          self._pdr.get_station_traffic_strength_dict()[
          sj_df["station_code"][j]])
      return l

    for i in range(n):
      l.append(
          self._pdr.get_station_traffic_strength_dict()[
          sj_df["station_code"][j-(i+1)]])
    return l

  def _get_n_prev_stn_tfc_col_names_list(self, n):
    """
    Returns a list ["tfc_of_stn_1", "tfc_of_stn_2" ...] upto value of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [("tfc_of_stn_"+str(i+1)) for i in range(n)]

  def _get_crnt_stn_tfc_col_names_list(self):
    return ["crnt_stn_tfc"]

  def _generate_n_prev_stn_dist_from_source_list(self, sj_df, j, n):
    """
    Returns a list containing n previous stations' distance from source for a
    given current station.

    Args:
      sj_df <pandas.DataFrame>: A single journey data frame.
      j <int>: The row index of the current station in sj_df whose n previous
               stations' distance from source is required.
      n <int>: Number of previous station codes.
    """
    l = []
    # If current station (i.e. n == 0)
    if n == 0:
      l.append(sj_df["distance"][j])
      return l

    for i in range(n):
      l.append(sj_df["distance"][j-(i+1)])
    return l

  def _get_n_prev_stn_dist_frm_src_col_names_list(self, n):
    """
    Returns a list ["stn_1_dist_frm_src", "stn_2_dist_frm_src" ...] upto value
    of n.

    Args:
      n <int>: Number of previous stations.
    """
    return [("stn_"+str(i+1)+"_dist_frm_src") for i in range(n)]

  def _get_crnt_stn_dist_frm_src_col_names_list(self):
    return ["crnt_stn_dist_frm_src"]

  def _generate_single_journey_df(self, df, i, source_rows):
    """
    Returns the single journey data frame starting at ith index in the source
    rows, out of the given data frame <df>

    Args:
      df <pandas.DataFrame>: the complete data frame of a train
      i <int>: ith index of source rows (rows at which journey info starts)
      source_rows <[...]>: the complete list of source rows in a train df i.e.
                           indices in the df where source station occurs for
                           each journey
    """
    sj_df = None
    if i == len(source_rows)-1:
      sj_df = df[source_rows[i]:df.shape[0]] #Single Journey DataFrame
    else:
      sj_df = df[source_rows[i]:source_rows[i+1]] #Single Journey DataFrame
    return sj_df

  def _get_column_names_list(self, n):
    """
    Returns a list of column headers in a data frame.

    Args:
      n <int>: Number of previous stations.
    """
    column_names_list = self._get_train_type_col_name_list()
    column_names_list.extend(self._get_zone_col_name_list())
    column_names_list.extend(self._get_is_superfast_col_name_list())
    column_names_list.extend(self._get_month_col_name_list())
    column_names_list.extend(self._get_weekday_col_name_list())
    column_names_list.extend(self._get_n_prev_stations_col_names_list(n))
    column_names_list.extend(self._get_n_prev_stn_late_mins_col_names_list(n))
    column_names_list.extend(self._get_n_prev_dist_bwn_stn_col_names_list(n))
    column_names_list.extend(self._get_n_prev_stn_dist_frm_src_col_names_list(n))
    column_names_list.extend(self._get_n_prev_stn_tfc_col_names_list(n))
    column_names_list.extend(self._get_n_prev_stn_deg_col_names_list(n))
    column_names_list.extend(self._get_crnt_stn_tfc_col_names_list())
    column_names_list.extend(self._get_crnt_stn_deg_col_names_list())
    column_names_list.extend(self._get_crnt_stn_dist_frm_src_col_names_list())
    column_names_list.extend(self._get_crnt_stn_late_mins_col_names_list())

    return column_names_list
