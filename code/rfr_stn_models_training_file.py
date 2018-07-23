#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file trains the Random Forest Regressor models for different
#       stations. Refer the reademe.txt in models/rfr_models/ to figure out the
#       correct combination of models and corresponding columns removed. Change
#       the directory arguments in the line where joblib is used to dump the
#       *.sav models.
#
#       Prints the RMSE of data frame on which training was done to see the fit.
#
#       To run this file execute:
#       python rfr_stn_models_training_file.py 1 1ps_rfr_labenc_models
#
#       where the numeral "1" can be changed as <1|2|3|4|5> as per the value of
#       "n" in n-previous-station models. The output trained models are saved in
#       "1ps_rfr_labenc_models" directory.
#
#       IMPORTANT NOTE: Make sure to remove the unwanted columns in data frame
#                       depending on experiments for which you want trained
#                       models. This can be done in function:
#                       "remove_unwanted_columns_df()" in "utilities/tt_utils.py".
#

import joblib
import pickle
import sys

from sklearn.ensemble import RandomForestRegressor as RFR
from sklearn.metrics import mean_squared_error

from utilities.tt_utils import TrainingTestUtils as TTU

if __name__ == "__main__":
  n = int(sys.argv[1]) # Get the n in "n previous station"
  mdl_output_dir = sys.argv[2] # Get the trained models output directory.
  ttu = TTU()
  stns = ttu._pdr.get_all_52trains_stations()
  stns_having_model = [] # Stations having n prev stations RFR models
  for s in stns:
    df = ttu._cdr.get_n_prev_station_csv_df(s, "complete_training", n)
    df = ttu._get_labenc_station_df(df, n)

    if not df.empty:
      stns_having_model.append(s)
      target_late_mins = df.pop("crnt_stn_late_mins")

      # Remove unwanted columns from the data frame
      df = ttu.remove_unwanted_columns_df(df, n)

      model = RFR(n_estimators=1000, n_jobs=-1, warm_start=True)
      model.fit(df, target_late_mins)
      pred_lms = model.predict(df)
      RMSE = mean_squared_error(target_late_mins, pred_lms)**0.5
      print s, RMSE

      joblib.dump(model, ttu._model_path + "rfr_models/" + mdl_output_dir +
                  "/" + s + "_label_encoding_model.sav")
  pickle.dump(stns_having_model, open(ttu._pdr._pdpath+
      "stations_having_"+str(n)+"ps_models.p", "wb"))
