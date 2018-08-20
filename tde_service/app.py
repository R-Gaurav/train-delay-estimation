#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# Desc: This file implements a flask REST API app for Train Delay Estimation.
#
# For multithreaded: http://flask.pocoo.org/docs/deploying/

import env

from datetime import datetime
from flask import Flask

import json
import pandas as pd
import re

from code.utilities.tt_utils import TrainingTestUtils as TTU
from tde_prediction import TDEPrediction as TDEP

from util import log

app = Flask(__name__)
pd.options.mode.chained_assignment = None  # Disable "SettingWithCopyWarning".

DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'
# Compile the regex since it is used multiple times in the life time of this app.
DATE_REGEX = re.compile(DATE_PATTERN)

# Instantiate following variables and keep them in memory because they are not
# going to change throughout the life time of this app.
ttu = TTU()
pdr = ttu._pdr

ALL_135_TRAINS = pdr.get_all_trains()

STNS_WITH_N_MDLS = {
  "1ps": pdr.get_stations_having_nps_model_list(nps=1),
  ## One can add more deeper models one may have tried. E.g., 2-order in next line
  # "2ps": pdr.get_stations_having_nps_model_list(nps=2)
}



# Route when only train number is passed.
@app.route("/<train_num>", defaults={"station": None, "date": None})
# Route when train number and a date is passed.
@app.route("/<train_num>/<date>", defaults={"station": None})
# Route when train number and station code is passed.
@app.route("/<train_num>/<station>/today", defaults={"date": None})
# Route when train number, station and date is passed.
@app.route("/<train_num>/<station>/<date>")
def accept_url(train_num, station, date):
  log.INFO("Train Number: %s, Station Code: %s, Date: %s"
           % (train_num, station, date))

  # Check for the validity of train number.
  if train_num not in ALL_135_TRAINS:
    log.ERROR("Train %s not in ALL_135_TRAINS list")
    return json.dumps({"Error": "Train: %s not accounted by our algorithm"
                      % train_num, "Result": None})

  if not date:
    date = str(datetime.now().date())

  # TODO Check for the validity of date (Also check for 12 months 31 days)
  # TODO Check for past dates and error out those as invalid.
  match = DATE_REGEX.match(date)
  if not match:
    log.ERROR("Date: %s is not valid as per regex")
    return json.dumps({"Error": "Date %s not correct" % date, "Result": None})

  lms_stns = TDEP().get_delay(STNS_WITH_N_MDLS, train_num, date, station)
  return json.dumps(lms_stns)

if __name__ == "__main__":
  app.run(threaded=True)
