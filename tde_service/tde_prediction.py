#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# This file implements the algorithm used to predict delays for a train at a
# particular station on a particular date.
#
import env

from datetime import datetime

from code.utilities.tt_utils import TrainingTestUtils as TTU

from util import log

class TDEPrediction(object):
  def __init__(self):
    self._ttu = TTU()
    self._cdr = self._ttu._cdr
    self._tdfu = self._ttu._tdfu
    self._month_dict = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
                        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
                        "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
    self._week_dict = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
                       4: "Friday", 5: "Saturday", 6: "Sunday"}

  def _get_modified_date_month_week_tuple(self, date):
    """
    Returns the month and weekday from the date.

    Args:
      date <str>: A valid date in "YYYY-MM-DD" in string format.
                  e.g. "2018-08-09".

    Returns:
      (str, str, str) i.e. (modified_date, month, weekday)
    """
    date = date.split("-")  #"2018-08-09" -> ['2018', '08', '09']
    weekday = self._week_dict[
        datetime(int(date[0]), int(date[1]), int(date[2])).date().weekday()]
    month = self._month_dict[date[1]]
    mod_date = date[2]+" "+month+" "+date[0]
    log.INFO("Modified Date: %s, Month: %s, Weekday: %s"
             % (mod_date, month, weekday))
    return (mod_date, month, weekday)

  def _get_trains_modified_journey_dataframe(self, train_num, date):
    """
    Returns a dataframe of the train `train_num` such that it has all the
    requried journey information and modified date, month and weekday column.

    Args:
      train_num <str>: A five digit train number e.g. "12307".
    """
    # TODO: Save some time here by having an updated latest journey dataframe.
    # Get the train's all journey data frame.
    train_df = self._cdr.get_train_complete_journey_df(train_num)
    # Extract the latest single journey data frame.
    source_rows = train_df[train_df.scharr == "Source"].index.tolist()
    train_latest_sj_df = self._tdfu._generate_single_journey_df(
        train_df, len(source_rows)-1, source_rows)
    num_rows_sj_df = train_latest_sj_df.shape[0]

    # TODO: Get a more accurate dateframe by incorporating actual previous dates
    # to the current queried date for a train which takes muliple days to
    # complete its journey. "day" column of dataframe might help.
    mod_date, month, weekday = self._get_modified_date_month_week_tuple(date)
    mod_date = [mod_date for _ in xrange(num_rows_sj_df)]
    month = [month for _ in xrange(num_rows_sj_df)]
    weekday = [weekday for _ in xrange(num_rows_sj_df)]

    # Modify the date columns.
    train_latest_sj_df["actarr_date"] = mod_date
    train_latest_sj_df["scharr_date"] = mod_date

    # Modify the month column.
    train_latest_sj_df["month"] = month

    # Modify the weekday column.
    train_latest_sj_df["weekday"] = weekday

    train_latest_sj_df = train_latest_sj_df.reset_index(drop=True)
    log.INFO("Train: %s single journey dataframe modified" % train_num)
    return train_latest_sj_df

  def get_delay(self, STNS_WITH_N_MDLS, train_num, date, station=None, nn=10,
                mdl="rfr", n=2):
    """
    Gets the delay for train `train_num` at station `station` on date `date`.

    Args:
      STNS_WITH_N_MDLS <dict>: A dict having values as list of stations with
                               n-prev-stns models.
      train_num <str>: A five digit train number e.g. "12307".
      date <str>: A date on which delays at stations are required,
                  e.g. "2018-07-08" in "YYYY-MM-DD" format.
      station <str>: A station code, e.g. "CNB".
      nn <int>: Number of nearest neighbour to be considered if the current
                station does not have n-prev-station models.
      mdl <str>: "rfr" for Random Forest Regressor models.
      n <int>: N in N-OMLMPF i.e. number of previous station to consider.

    Returns:
      dict:

      {
        "Error": <None> or <str: Error Message>,
        "Result": <dict: A dict of station_codes as keys and predicted late
                  minutes as values.
      }
    """
    # Get the train's journey information.
    ret = {"Error": None, "Result": None}
    try:
      train_sj_df = self._get_trains_modified_journey_dataframe(train_num, date)
    except Exception as e:
      log.ERROR("Error occurred for train: %s, Error type: %s, Error message: %s"
                % (train_num, type(e), str(e)))
      ret["Error"] = str(e)
      return ret

    inline_stns = train_sj_df["station_code"].tolist()
    # Store the predicted late minutes at inline stations in a list.
    lms_at_stns = [0]

    for index in range(1, len(inline_stns)):
      # TODO: In case a station is given, can we exit the for loop, once late
      # minutes for the queried station is predicted?
      stn = inline_stns[index]
      try:
        if (index == 1 or n == 1): # Valid for only 1 previous station.
          # Get the nearest neighbour station to current station it has no models.
          if stn not in STNS_WITH_N_MDLS["1ps"]:
            stn = self._ttu.get_station_nearest_neighbors_list(stn, 1, nn)[0]

          # Pass the `index` of current station `stn` to make its row data frame
          # and station code `stn` whose model would be used to predict late
          # minutes. In case of a Known Station, `stn` and its `index` would
          # represent the same station, in case of Unknown Station or Station
          # with no models, `stn` would be the nearest neighbour station, however
          # the `index` would make sure that the row data frame is calculated for
          # the correct current station.
          plm = self._ttu.get_predicted_late_mins_at_station_float(
              train_num, train_sj_df, index, 1, stn, lms_at_stns, index, mdl)
          lms_at_stns.append(plm)
          continue

        if (index == 2 or n == 2): # Valid for only 2 previous stations.
          if stn not in STNS_WITH_N_MDLS["2ps"]:
            stn = self._ttu.get_station_nearest_neighbors_list(stn, 2, nn)[0]
          plm = self._ttu.get_predicted_late_mins_at_station_float(
              train_num, train_sj_df, index, 2, stn, lms_at_stns, index, mdl)
          lms_at_stns.append(plm)
          continue

        if (index == 3 or n == 3): # Valid for only 3 previous stations.
          if stn not in STNS_WITH_N_MDLS["3ps"]:
            stn = self._ttu.get_station_nearest_neighbors_list(stn, 3, nn)[0]
          plm = self._ttu.get_predicted_late_mins_at_station_float(
              train_num, train_sj_df, index, 3, stn, lms_at_stns, index, mdl)
          lms_at_stns.append(plm)
          continue

        if (index == 4 or n == 4): # Valid for only 4 previous stations.
          if stn not in STNS_WITH_N_MDLS["4ps"]:
            stn = self._ttu.get_station_nearest_neighbors_list(stn, 4, nn)[0]
          plm = self._ttu.get_predicted_late_mins_at_station_float(
              train_num, train_sj_df, index, 4, stn, lms_at_stns, index, mdl)
          lms_at_stns.append(plm)
          continue

        if (index == 5 or n == 5): # Valid for only 5 previous stations.
          if stn not in STNS_WITH_N_MDLS["5ps"]:
            stn = self._ttu.get_station_nearest_neighbors_list(stn, 5, nn)[0]
          plm = self._ttu.get_predicted_late_mins_at_station_float(
              train_num, train_sj_df, index, 5, stn, lms_at_stns, index, mdl)
          lms_at_stns.append(plm)

      except Exception as e:
        log.WARN("Error occurred for train: %s, Error type: %s, Error message: %s"
                 % (train_num, type(e), str(e)))
        lms_at_stns.append(plm)

    lms_at_stns_dict = {} # Store the predicted late minutes in a dict.
    for index in range(len(inline_stns)):
      lms_at_stns_dict[inline_stns[index]] = lms_at_stns[index]

    if station:
      try:
        ret["Result"] = {station: lms_at_stns_dict[station]}
      except Exception as e:
        log.ERROR("Error occurred for train: %s, Error type: %s, "
                  "Error message: %s" % (train_num, type(e), str(e)))
        ret["Error"] = ("Queried station: %s not found along the journey of "
                        "train: %s. It may be because of the stale journey "
                        "information of train: %s in database."
                        % (station, train_num, train_num))
        ret["Result"] = None
      return ret

    ret["Result"] = lms_at_stns_dict
    return ret
