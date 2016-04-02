#!/usr/bin/env python

import glob
import re
import logging
import shutil
import os

from tsg.intermediate import generate_intermediate
from tsg.config import PARSED_DIR, INTERMEDIATE_DIR

logging.basicConfig(level=logging.INFO)


def main():
    print('Do you want to delete intermediate/ ? y/N')
    if input() == 'y':
        shutil.rmtree(INTERMEDIATE_DIR)
        os.mkdir(INTERMEDIATE_DIR)

    files = glob.glob(PARSED_DIR + '*.json')
    for f in files:
        try:
            uuid = re.search('([^/]*).json$', f).groups()[0]
        except AttributeError:
            continue

        generate_intermediate(uuid)


if __name__ == "__main__":
    main()
