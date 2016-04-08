import math
import glob
import logging
import re
import json

import pandas as pd
import numpy as np


def parse_term(term_file, N):
    '''
    N: number of documents in total
    '''
    term_df = pd.read_csv(term_file, index_col='uuid')

    # count per document
    term_df['sum'] = term_df.sum(axis=1)
    term_df['tf-idf'] = (np.log10(term_df['sum'])+1)*math.log10(N/len(term_df))

    term_df.sort_values('tf-idf', ascending=False, inplace=True)

    pairs = term_df.apply(lambda row: '{}:{}'.
                          format(row.name, row['tf-idf']),
                          axis=1)
    return ",".join(pairs)


def create_index(intermediate_dir,
                 num_documents,
                 dictionary_path,
                 indexinfo_path):

    # find all csvs and sort them alphabetically
    files = glob.glob(intermediate_dir+'*.csv')
    files.sort()

    # TODO: move this to indexer
    compiled_termname_re = re.compile('([^/]*).csv')
    with open(dictionary_path, 'w') as dictionary_file:  # deletes dictionary!
        for term_file in files:
            term = compiled_termname_re.search(term_file).groups()[0]
            indexed_line = parse_term(term_file, num_documents)

            dictionary_file.write('{} {}\n'.format(term, indexed_line))
            logging.info('Indexed term {}'.format(term))

    create_indexinfo(num_documents, indexinfo_path)


def create_indexinfo(num_documents, indexinfo_path):
    obj = {'num_documents': num_documents}
    with open(indexinfo_path, 'w') as f:
        json.dump(obj, f)


def hash_index():
    pass
