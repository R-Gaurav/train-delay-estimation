#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file analyses the results
#

import joblib
import numpy as np
import os
import pandas as pd
from scipy import stats

from utilities.tt_utils import TrainingTestUtils as TTU

class ResultAnalysis(object):
  def __init__(self):
    self._ttu = TTU()
    self._cdr = self._ttu._cdr
    self._pdr = self._ttu._pdr

  def get_confidence_intervals_train_stations_df_dict(self, train_num,
      ci_prob=0.95):
    """
    Returns a df of CI of all known 52 trains stations, complete journey is
    considered. DF is dict of station vs CIs for the given train.

    Args:
      train_num <string>: Train number eg. "12307"
      ci_prob <float>: The Confidence Interval probability. <0..1>
    """
    stns_stats_dict = {}
    train_df = self._cdr.get_train_complete_journey_df(train_num)
    # Get all the unique stations whose CI has to be calculated monthly.
    unq_stns = train_df.station_code.unique()

    # Get all the unique months for whom CI for a station would be calculated.
    unq_mnts = train_df.month.unique()

    stn_stats_cols = ["month", "mean_lms", "std", "ci"]
    # Calculate CI for each stations.
    for stn in unq_stns:
      # Select the data frame for the current station
      stn_df = train_df[train_df.station_code == stn]
      stn_stats_df = []
      # Calculate for every month.
      for mnt in unq_mnts:
        # Select the data frame out of stn_df for the current month.
        stn_mnt_df = stn_df[stn_df.month == mnt]
        if not stn_mnt_df.empty:
          # If the stn_mnt_df is not empty, remove outliers by Tukeys Rule.
          first_q = np.percentile(stn_mnt_df.latemin, 25)
          third_q = np.percentile(stn_mnt_df.latemin, 75)
          iqr = third_q - first_q
          upr_threshold = third_q + 1.5*iqr # Factor of 1.5 can be changed to 3.
          # Not calculating lower threshold since trains can arrive on time at
          # the stations in best cases.
          # Select cleaned stn_mnt_df by removing outliers (outlier late mins
          # due to trains being late at the source).
          cln_stn_mnt_df = stn_mnt_df[stn_mnt_df.latemin <= upr_threshold]
          mean_lms = cln_stn_mnt_df.latemin.mean()
          std = cln_stn_mnt_df.latemin.std()
          # Calculate length of late minutes list for which mean is calculated.
          len_lml = len((cln_stn_mnt_df.latemin.tolist()))
          ci = stats.t.interval(ci_prob, len_lml-1, loc=mean_lms,
              scale=std/np.sqrt(len_lml))
        else: # If the stn_mnt_df is empty.
          mean_lms = -1
          std = -1
          ci = (-1, -1)
        stn_stats_df.append([mnt, mean_lms, std, ci])
      stn_stats_df = pd.DataFrame(stn_stats_df, columns = stn_stats_cols)
      stns_stats_dict[stn] = stn_stats_df
    return stns_stats_dict

  def find_ci_probability_of_pred_lms_df(self, train_num, ci_prob=0.95, nps=4,
      rfr_mdl="", group="known"):
    """
    Returns total number of predictions and number of predictions of
    late minutes at stations within CI ci_prob.

    Args:
      train_num <string>: Train number eg. "12307".
      ci_prob <float>: The Confidence Interval probability. <0..1>
      nps <int>: number of previous stations
      rfr_mdl <string>: <""|"without_nps_codes"|"wonps_wdts">
      group <string>: <"known"|"unknown">
    """
    # If the predicted late minutes for a station falls in its CI of fixed
    # ci_prob say 0.95, then there is 95% chance that the train will get delayed
    # by that many predicted late minutes at the chosen station.

    # Get the train's data frame for cross validation.
    train_df = self._cdr.get_train_journey_df(train_num, "unknown_test")
    # Get the predicted late minutes for the train's cross validation data.
    pred_lms_df = self._cdr.get_jw_pred_late_mins_of_train_df(train_num, nps,
        rfr_mdl, group)
    # Remove "JRNY END" rows from pred_lms_df.
    pred_lms_df = pred_lms_df.loc[~pred_lms_df.Stations.isin(["JRNY END"])]
    # Get the CI for the train's stations.
    stns_stats_dict = self.get_confidence_intervals_train_stations_df_dict(
        train_num, ci_prob)

    total_predictions = len(train_df)
    num_of_ci_prob_preds = 0

    for i in range(total_predictions):
      # Select the month in which late mins is predicted for the station.
      mnt = train_df.iloc[i].month
      stn = train_df.iloc[i].station_code
      pred_lms = float(pred_lms_df.iloc[i].PredictedLateMins)

      # Select the stations CI from stns_stats_dict.
      try:
        stn_stats = stns_stats_dict[stn]
      except:
        continue
      stn_month_stats = stn_stats[stn_stats.month==mnt]
      stn_month_stats_ci = tuple(stn_month_stats["ci"])
      try:
        if (pred_lms >= stn_month_stats_ci[0][0] and
            pred_lms <= stn_month_stats_ci[0][1]):
          num_of_ci_prob_preds += 1
      except:
        print stn_month_stats, pred_lms

    return total_predictions, num_of_ci_prob_preds

  def calculate_diff_of_af_df_and_nf_df(self, ci_prob):
    """
    Calculates the difference of "%_preds_within_ci" in additional features (af)
    data frame and in normal features (nf) data frame and saves it in CSV files.

    Args:
      ci_prob <float>: The confidence interval probability. [0..1]
    """
    file_path = self._cdr._cdpath + "analysed_data/known_trains/"

    files = os.listdir(file_path)
    CI = str(int(ci_prob * 100))
    diff_df = []
    diff_df_cols = ["train_number", "1ps", "2ps", "3ps", "4ps", "5ps"]
    nf_df = pd.DataFrame()
    af_df = pd.DataFrame()

    for f in files:
      if f.startswith("CI"+CI):
        df = pd.read_csv(file_path+f)
        temp_df = pd.DataFrame()
        temp_df[f[13:16]] = df["%_preds_within_ci"]
        if f.endswith("model.csv"): # Info corresponding to normal features df.
          nf_df = pd.concat([nf_df, temp_df], axis=1)
        else: # Info corresponding to additional features df.
          af_df = pd.concat([af_df, temp_df], axis=1)

    diff_df = af_df - nf_df
    diff_df["train_number"] = pd.read_csv(file_path+files[0])["train_number"]
    diff_df = diff_df[["train_number", "1ps", "2ps", "3ps", "4ps", "5ps"]]
    desc = diff_df.describe()
    diff_df.to_csv(file_path+"CI"+CI+"diff_bwn_af_nf_results.csv")
    desc.to_csv(file_path+"CI"+CI+"diff_stats.csv")

  def calculate_AIC_or_BIC_float(self, train_num, nps, rfr_mdl="", group=""):
    """
    Calculates BIC value of model determined by nps for different test settings.
    http://www.stat.wisc.edu/courses/st572-larget/Spring2007/handouts09-4.pdf
    Uncomment the formula for calculating either AIC or BIC accordingly.

    Args:
      train_num <string>: Train Number for whom BIC is needed. eg. "12307"
      nps <int>: Number of previous stations
      rfr_mdl <string>: <""|"_wonps_wdts">
      group <string>: <"known"|"unknown">
    """
    jw_lms_df = self._cdr.get_jw_pred_late_mins_of_train_df(train_num, nps,
        rfr_mdl, group)
    # Load any nps model to get the number of parameters or features
    model = joblib.load(self._ttu._model_path+"rfr_models/"+str(nps)+"ps_rfr"+
        "_labenc_models_complete"+rfr_mdl+"/CNB_label_encoding_model.sav")

    # Remove "JRNY END" rows from pred_lms_df.
    jw_lms_df = jw_lms_df.loc[~jw_lms_df.Stations.isin(["JRNY END"])]
    # Calcuate Residual Sum of Squares (also known as Sum of Squared Errors)
    actual_lms = jw_lms_df.ActualLateMins.astype(dtype=float)
    pred_lms = jw_lms_df.PredictedLateMins.astype(dtype=float)
    error = actual_lms - pred_lms
    sqrd_error = error ** 2
    rss = np.sum(sqrd_error) # Calculate RSS
    num_of_obsrs = jw_lms_df.shape[0] # Calculate Number of Observations
    num_of_parms = model.n_features_

    #BIC = (num_of_obsrs * np.log((rss * 1.0)/num_of_obsrs) +
    #    num_of_parms * np.log(num_of_obsrs))
    #return BIC

    AIC = (num_of_obsrs * np.log((rss * 1.0)/num_of_obsrs) +
        num_of_parms * 2)
    return AIC

  def save_bic_df_and_calc_nps_with_minimum_bic_int(
      self, rfr_mdl="", group=""):
    """
    Saves the BIC lists into a df and calculates the value nps which has minimum
    bic. This function acts generic depending on the value (either AIC or BIC)
    returned by function calculate_AIC_or_BIC_float. Do not confuse with the
    name of the function that it saves only BIC data frames, it is generic.
    Change the name of saved data frame file in last line  accordingly.

    Args:
      rfr_mdl <string>: <""|"_wonps_wdts">
      group <string>: <"known"|"unknown">
    """
    df = []
    columns = ["TrainNum", "1OR", "2OR", "3OR", "4OR", "5OR", "Min_n"]
    all_trains = self._pdr.get_all_trains()[52:] # All Known Trains
    for train in all_trains:
      bic_list = [train]
      min_i = 1
      min_b = None
      for i in range(1,6):
        BIC = self.calculate_AIC_or_BIC_float(train, i, rfr_mdl, group)
        bic_list.append(BIC)
        if i == 1:
          min_i = 1
          min_b = BIC
        else:
          if BIC < min_b:
            min_i = i
            min_b = BIC
      bic_list.append(min_i)
      df.append(bic_list)
    df = pd.DataFrame(df, columns=columns)
    df.to_csv(self._cdr._cdpath+"analysed_data/"+group+"_trains/aic_analysis/"+
        group+rfr_mdl+".csv", index=False)

  def calculate_sum_of_rmses_for_n_omlmpf_df(self, group, rfr_mdl=""):
    """
    Caculcates and saves the total RMSE for all trains in different rfr_mdl
    settings for different values of n in different groups. This gives the
    overall measure of the performance of different N-OMLMPF, pointing out
    the one with minimum overall RMSE, thus used during production mode.

    Args:
      group <string>: <"known">
      rfr_mdl <string>: <""|"_wonps_wdts">
    """
    df = []
    columns = [
        "Train", "1-OMLMPF", "2-OMLMPF", "3-OMLMPF", "4-OMLMPF", "5-OMLMPF"]
    trains = self._pdr.get_all_trains()[:52]
    for train in trains:
      train_wise_sum_rmse = [train]
      for i in range(5):
        rmse_list = self._pdr.get_rmse_of_journey_wise_lms_pred_list(
            i+1, group, train, rfr_mdl=rfr_mdl)
        train_wise_sum_rmse.append(sum(rmse_list))
      df.append(train_wise_sum_rmse)
    df = pd.DataFrame(df, columns=columns)
    df.to_csv(self._cdr._cdpath+"analysed_data/"+group+"_trains/sum_rmse_of_"+
              group+"_trains_"+rfr_mdl+".csv", index=False)

if __name__ == "__main__":

  # Uncomment the codes in different blocks to run any specific data analysation
  # code.
  ra = ResultAnalysis()

  ##############################################################################
  """
  group = "test_unknown"
  nps = 5
  rfr_mdl = "_wonps_wdts"
  all_trains = ra._pdr.get_all_trains()[52:] # Known Trains
  train_ci_df_cols = ["train_number", "#_preds", "#_preds_within_ci",
      "%_preds_within_ci"]

  for ci_prob in [0.68, 0.95, 0.99]:
    train_ci_df = []
    for train in all_trains:
      (total_predictions, num_of_ci_prob_preds) = (
          ra.find_ci_probability_of_pred_lms_df(train, ci_prob, nps, rfr_mdl,
                                                group))
      try:
        train_ci_df.append([train, total_predictions, num_of_ci_prob_preds,
            num_of_ci_prob_preds*100.0/total_predictions])
      except:
        print train, total_predictions, num_of_ci_prob_preds
    train_ci_df = pd.DataFrame(train_ci_df, columns = train_ci_df_cols)
    train_ci_df.to_csv(ra._cdr._cdpath+"rmr_analysed_data/"+group+"_trains/CI"+
        str(int(ci_prob * 100))+"_results_"+str(nps)+"ps_rmr_5e_1_model"+
        rfr_mdl+".csv", index=False)
  """
  ##############################################################################
  """
  ra.calculate_diff_of_af_df_and_nf_df(0.99)
  """
  ##############################################################################

  ra.save_bic_df_and_calc_nps_with_minimum_bic_int("_wonps_wdts", "test_unknown")

  ##############################################################################
  """
  ra.calculate_sum_of_rmses_for_n_omlmpf_df("known", "_wonps_wdts")
  """
