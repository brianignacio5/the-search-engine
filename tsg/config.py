import os
import shutil
import sys
from os.path import expanduser

TESTING = sys.argv[0].endswith('nosetests')
if TESTING:
    DATA_DIR = '/tmp/tsgtest123aeiae31ea/'
    shutil.rmtree(DATA_DIR, ignore_errors=True)
else:
    # DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/../data/'
    DATA_DIR = expanduser("~") + '/tsgdata/'

RAW_DIR = DATA_DIR + 'raw/'
PARSED_DIR = DATA_DIR + 'parsed/'
INTERMEDIATE_DIR = DATA_DIR + 'intermediate/'

# create necessary file structure
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)
os.makedirs(INTERMEDIATE_DIR, exist_ok=True)

FIELDS = ['type', 'title', 'isbn', 'content']
CSV_HEADER = ','.join(['uuid'] + FIELDS)

DICTIONARY_PATH = DATA_DIR + 'dictionary.dat'
INDEXINFO_PATH = DATA_DIR + 'indexinfo.json'

THROTTLE_SECONDS = 1.6  # default throttle time, gets replaced by robots.txt,
                        # parsing
ALLOWED_SITES = []
DISALLOWED_SITES = []
