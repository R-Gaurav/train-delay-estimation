#
# Train Delay Estimation
#
# Author: gaurav.ramashish@gmail.com
#
# This file implements the algorithm used to predict delays for a train at a
# particular station on a particular date.
#
import env

from util import log
from code.utilities.df_utils import TrainDataFrameUtils as TDFU

class TDEPrediction(object):
  def __init__(self):
    pass

  def bar(self):
    log.INFO("Hello")

    log.WARN("How")

    try:
      1/0
    except Exception as e:
      log.ERROR("Are you: %s" % e)

if __name__ == "__main__":
  ob = TDEPrediction()
  ob.bar()
