#!/usr/bin/env python

import glob
import re
import logging
import shutil
import os

from tsg.indexer import index
from tsg.config import INTERMEDIATE_DIR, DICTIONARY_PATH

logging.basicConfig(level=logging.INFO)


def main():
    print('Careful, this deletes data/parsed/*. Wanna proceed? y/N')
    if input() != 'y':
        return

    shutil.rmtree(PARSED_DIR)
    os.mkdir(PARSED_DIR)

    files = glob.glob(RAW_DIR + '*.html')
    for f in files:
        try:
            document_type = re.search('([^/_]*)[^/]*.html$', f).groups()[0]
        except AttributeError:
            continue

        parse_document(document_type, f)


if __name__ == "__main__":
    main()
