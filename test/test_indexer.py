import os
import math
import json

import pandas as pd
import numpy as np
from nose.tools import eq_
from nose import with_setup
import mock


from tsg.config import DATA_DIR, FIELD_WEIGHTS
from tsg.indexer.base import parse_term, hash_index,\
    create_index, create_indexinfo


def test_parse_term():
    TERM = 'aa'
    term_file = 'test/files/{}.csv'.format(TERM)
    N = 3

    # These values are taken from aa.csv directly
    w1count = (np.array([0, 1, 0, 3]) * FIELD_WEIGHTS).sum()
    w2count = (np.array([0, 1, 0, 1]) * FIELD_WEIGHTS).sum()

    qscores = pd.DataFrame({'qscore': [0.75, 2/3]},
                           index=['598859a0-eaa7-466a-8919-e6260c89edef',
                                  '31a8e3b4-8c67-4fb7-b11a-1df1105617a2'])
    qscores.index.name = 'uuid'

    pagerank_scores = pd.DataFrame({'pagerank_score': [5, 1]},
                                   index=['598859a0-eaa7-466a-8919-e6260c89edef',
                                          '31a8e3b4-8c67-4fb7-b11a-1df1105617a2'])
    pagerank_scores.index.name = 'uuid'

    # scale pagerank_scores
    scaled_pagerank_scores = np.log10(pagerank_scores)
    scaled_pagerank_scores += 1 - np.min(scaled_pagerank_scores)#


    termline = parse_term(term_file, N, qscores, pagerank_scores)

    w1 = (1+math.log10(w1count)) * \
        (1+math.log10(N/2)) * \
        qscores.loc['598859a0-eaa7-466a-8919-e6260c89edef'].qscore * \
        scaled_pagerank_scores.loc['598859a0-eaa7-466a-8919-e6260c89edef'].pagerank_score

    w2 = (1+math.log10(w2count)) * \
        (1+math.log10(N/2)) * \
        qscores.loc['31a8e3b4-8c67-4fb7-b11a-1df1105617a2'].qscore * \
        scaled_pagerank_scores.loc['31a8e3b4-8c67-4fb7-b11a-1df1105617a2'].pagerank_score

    # overwrite weights because of numerical issue
    #w2 = 0.18126459066485565

    eq_(termline,
        '598859a0-eaa7-466a-8919-e6260c89edef:{},'
        '31a8e3b4-8c67-4fb7-b11a-1df1105617a2:{}'.format(w1, w2))


TEST_DICT_PATH = DATA_DIR + 'testdict.dat'
TEST_INDEXINFO_PATH = DATA_DIR + 'testinfo.json'


def clean_testfiles():
    for f in [TEST_DICT_PATH, TEST_INDEXINFO_PATH]:
        try:
            os.remove(TEST_DICT_PATH)
        except FileNotFoundError:
            pass


@with_setup(clean_testfiles, clean_testfiles)
@mock.patch('tsg.indexer.base.create_indexinfo')
def test_create_index(create_indexinfo_mock):
    num_documents = 3
    # TODO add some files to test/files/intermediate and check the dictionary
    # later
    create_index('test/files/intermediate/',
                 'test/files/parsed',
                 num_documents,
                 TEST_DICT_PATH,
                 TEST_INDEXINFO_PATH,
                 'test/files/qscores_a.csv',
                 'test/files/pagerank_a.csv')

    assert os.path.isfile(TEST_INDEXINFO_PATH)
    create_indexinfo_mock.assert_called_with(num_documents, TEST_INDEXINFO_PATH)


@with_setup(clean_testfiles, clean_testfiles)
def test_create_indexinfo():
    num_documents = 3
    create_indexinfo(3, TEST_INDEXINFO_PATH)

    assert os.path.isfile(TEST_INDEXINFO_PATH)
    with open(TEST_INDEXINFO_PATH) as f:
        assert json.load(f) == {'num_documents': num_documents}


def test_hash_index():
    hash_index()
    # TODO
