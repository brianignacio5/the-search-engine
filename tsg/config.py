import os
# import shutil

# if os.getenv('ENVIRONMENT') == 'TEST':
#     DATA_DIR = '/tmp/tsgtest123aeiae31ea/'
#     shutil.rmtree(DATA_DIR)
# else:
DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/../data/'

RAW_DIR = DATA_DIR + 'raw/'
PARSED_DIR = DATA_DIR + 'parsed/'
INTERMEDIATE_DIR = DATA_DIR + 'intermediate'

# create necessary file structure
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)
os.makedirs(INTERMEDIATE_DIR, exist_ok=True)
