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

# Here "train-delay-estimation-ITSC2018" is downloaded in "/Personal/projects/".
# Here "data" is downloaded in "/Personal/projects/train-delay-estimation-ITSC2018/".
# Here "models" is set in "/Personal/projects/train-delay-estimation-ITSC2018/".

project_dir_path = "/Personal/tmp/train-delay-estimation-ITSC2018/"

# Insert the path to the project directory in sys.path so that subdirectories
# and code files are accessible in other files.
sys.path.insert(0, project_dir_path+"code/")

# Insert the path to readers directory.
sys.path.insert(0, project_dir_path+"code/readers/")

# Insert the path to the data (input) directory.
# data_path contains all the raw data and pickle data.
data_path = project_dir_path+"data/"

# Insert the path to the trained models of stations (output) directory.
models_path =  project_dir_path+"models/"
