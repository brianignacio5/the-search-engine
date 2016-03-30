import os
import shutil
import sys

TESTING = sys.argv[0].endswith('nosetests')
if TESTING:
    DATA_DIR = '/tmp/tsgtest123aeiae31ea/'
    shutil.rmtree(DATA_DIR, ignore_errors=True)
else:
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/../data/'

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
THROTTLE_SECONDS = 1.6
