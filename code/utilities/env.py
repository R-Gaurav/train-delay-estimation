#
# Train Delay Estimation Project
#
# author: gaurav.ramashish@gmail.com
#
# This module sets up paths for different directories of data and saved models.
# Import this file always at the beginning of each file.
#

import sys

# This module should NOT be executed.
assert __name__ != "__main__"

# Set up the local path (in your machine) to the directory where you downloaded
# the TrainDelayEstimation git repository.
# Here "TrainDelayEstimation" is downloaded in "/Personal/projects/".
# Here "data" is downloaded in "/Personal/projects/".
# Here "models" is set in "/Personal/projects/".

project_dir_path = "/home/raga/tde/"

# Insert the path to the project directory in sys.path so that subdirectories
# and code files are accessible in other files.
sys.path.insert(0, project_dir_path+"TrainDelayEstimation/")

# Insert the path to readers directory.
sys.path.insert(0, project_dir_path+"TrainDelayEstimation/readers/")

# Insert the path to the data (input) directory.
# data_path contains all the raw data and pickle data.
data_path = project_dir_path+"data/"

# Insert the path to the trained models of stations (output) directory.
models_path =  project_dir_path+"models/"
