#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# Desc: This file trains linear models for 596 known stations. But the linear
#       models trained were not found to be robust during evaluation and
#       prediction.
#       Therefore not an important file with view of training and testing the
#       late minutes prediction framework.
#
#       To run this file execute:
#       python lmr_stn_models_training_file.py 1
#
#       where the numeral "1" can be changed to <1|2|3|4|5> depending on the "n"
#       in n-previous-station models.
#

import joblib
import pickle
import sys

from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.metrics import mean_squared_error

from utilities.tt_utils import TrainingTestUtils as TTU

if __name__ == "__main__":
  n = int(sys.argv[1])
  ttu = TTU()
  stns = ttu._pdr.get_all_52trains_stations()
  stns_having_model = []
  for s in stns:
    df = ttu._cdr.get_n_prev_station_csv_df(s, "complete_training", n)
    df = ttu._get_labenc_station_df(df, n)

    if not df.empty:
      stns_having_model.append(s)
      target_late_mins = df.pop("crnt_stn_late_mins")

      # Remove unwanted columns from the data frame
      df = ttu.remove_unwanted_columns_df(df, n)

      model = LinearRegression(n_jobs=-1)
      model.fit(df, target_late_mins)
      pred_lms = model.predict(df)
      RMSE = mean_squared_error(target_late_mins, pred_lms)**0.5
      print "Linear Regression: ", s, RMSE

      joblib.dump(model, ttu._model_path+"lmr_models/"+str(n)+
          "ps_lmr_labenc_models_complete_wonps_wdts/"+s+
          "_label_encoding_model.sav")
  pickle.dump(stns_having_model, open(ttu._pdr._pdpath+"stations_having_"+
      str(n)+"ps_lmr_models_complete_wonps_wdts.p", "wb"))

