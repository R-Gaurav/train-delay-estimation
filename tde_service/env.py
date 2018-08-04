#
# Train Delay Estimation Project
#
# Author: gaurav.ramashish@gmail.com
#
# This module sets up the environment for running the TDE Service.
#

import sys

# This module should NOT be executed.
assert __name__ != "__main__"

# Set up the project directory.
project_dir_path = "/Personal/train-delay-estimation/"

# Insert the project directory path in sys.path, so that subdirecotries and code
# files therein are able to access the other (top level) files.
sys.path.insert(0, project_dir_path)
