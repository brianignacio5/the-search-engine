#!/usr/bin/env python

import glob
import re
import logging

from tsg.indexer import parse_term
from tsg.config import RAW_DIR, INTERMEDIATE_DIR, DICTIONARY_PATH

logging.basicConfig(level=logging.INFO)


def main():
    # find all csvs and sort them alphabetically
    files = glob.glob(INTERMEDIATE_DIR+'*.csv')
    files.sort()

    num_documents = len(glob.glob(RAW_DIR+'*.html'))

    print('Careful, this deletes the index. Wanna proceed? y/N')
    if input() != 'y':
        return

    # TODO: move this to indexer
    compiled_termname_re = re.compile('([^/]*).csv')
    with open(DICTIONARY_PATH, 'w') as dictionary_file:  # deletes dictionary!
        for term_file in files:
            term = compiled_termname_re.search(term_file).groups()[0]
            indexed_line = parse_term(term_file, num_documents)

            dictionary_file.write('{} {}\n'.format(term, indexed_line))
            logging.info('Indexed term {}'.format(term))


if __name__ == "__main__":
    main()
