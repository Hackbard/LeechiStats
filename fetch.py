__author__ = "Benjamin Klein"
__maintainer__ = "Benjamin Klein"
__email__ = "hackbard23@gmail.com"
__copyright__ = "Copyright 2018"
__license__ = "GNU GPL v3"
__version__ = "0.0.1"

from Fetcher import Fetcher
from os import path, remove

# File with one url per line
INPUT_FILE = "input.txt"
# file to keep only one job running
ALREADY_RUNNING_FILE = '.running'

if path.exists(ALREADY_RUNNING_FILE):
    print("Already running")
    exit(1)

# open(ALREADY_RUNNING_FILE, 'a').close()

if __name__ == "__main__":
    targets = []
    with open(INPUT_FILE) as file:
        read_data = file.read()
        targets = read_data.split("\n")
    file.close()
    # Fetcher
    f = Fetcher()
    f.setTargets(targets)
    f.execute()

# remove(ALREADY_RUNNING_FILE)