import math

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


def hash_index():
    pass
