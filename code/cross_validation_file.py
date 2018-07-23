#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file evaluates the trained Random Forest models for each stations.
#       Refer readme.txt in models/rfr_models/ to get the appropriate columns in
#       data frame, hence the corresponding model ("", "_without_nps_codes",
#       "_wonps_wdts"). Change the last line of pickle dump accordingly as
#       columns removed.
#       Not an important file from point of view of training the models and
#       testing the late minutes prediction framework.
#
#       To run the file, execute:
#       python cross_validation_file.py rfr 2
#
#       where the "rfr" can be changed to "lmr" and numeral can be changed to
#       <1|2|3|4|5> for different n_prev_station models to be cross-validated
#       (not to predict late minutes during journey). "rfr" stands for random
#       forest regressor models and "lmr" stands for linear model regressors.
#
#       NOTE: This file is only meant to analyse the performance of late mins
#             prediction, so data frame is passed to trained models in batch set
#             instead of row wise (hence no filling of predicted late mins at
#             previous stations as done in N-OMLMPF algorithm).
#
import joblib
import pickle
import sys

from utilities.tt_utils import TrainingTestUtils as TTU
from sklearn.metrics import mean_squared_error

if __name__ == "__main__":
  mdl = sys.argv[1]
  n = int(sys.argv[2])
  ttu = TTU()
  stns = ttu._pdr.get_all_52trains_stations()
  rmse_list = []

  for s in stns:
    df = ttu._cdr.get_n_prev_station_csv_df(s, "cross_validation", n)
    df = ttu._get_labenc_station_df(df, n)

    if not df.empty:
      actual_late_mins = df.pop("crnt_stn_late_mins")

      # Remove unwanted columns from the data frame
      df = ttu.remove_unwanted_columns_df(df, n)

      pred_late_mins = ttu.get_predicted_late_mins_list(s, n, df, mdl)
      RMSE = mean_squared_error(actual_late_mins, pred_late_mins)**0.5
      # Create a list of Station and corresponsing RMSE
      rmse_list.append([s, RMSE])
      print s, RMSE
  # Dump the cross validation label encoding rmse list
  pickle.dump(
      rmse_list, open(ttu._pdr._pdpath+str(n)+"ps_cv_labenc_rmse_list.p", "wb"))
