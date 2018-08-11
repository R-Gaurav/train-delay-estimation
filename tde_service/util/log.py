#
# Train Delay Estimation Project
#
# Author: Ramashish Gaurav
#
# Log file utilities.
#

from os import path, remove

import logging
import traceback

 # Name of the log file where all messages would be logged.
LOG_FILE = "logs/tde_logs.log"

# If applicable, delete the existing log file to generate a fresh log file i
# during each execution
if path.isfile(LOG_FILE):
    remove(LOG_FILE)

# Create the logger
logger = logging.getLogger(__name__)
# Set the logging level to DEBUG, such that all level messages are logged.
logger.setLevel(logging.DEBUG)

# Create handler for logging the messages to a log file.
log_handler = logging.FileHandler(LOG_FILE)
log_handler.setLevel(logging.DEBUG)

# Set the format of the log.
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Add the Formatter to the Handler
log_handler.setFormatter(log_formatter)

# Add the Handler to the Logger
logger.addHandler(log_handler)
logger.info('Completed configuring logger()!')

def INFO(msg):
  logger.info(msg)

def WARN(msg):
  logger.warning(msg)
  logger.warning(traceback.format_exc())

def ERROR(msg):
  logger.error(msg)
  logger.error(traceback.format_exc())
