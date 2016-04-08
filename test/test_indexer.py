import os
import math
import json

from nose.tools import eq_
from nose import with_setup
import mock


from tsg.config import DATA_DIR
from tsg.indexer.base import parse_term, hash_index,\
    create_index, create_indexinfo


def test_parse_term():
    TERM = 'aa'
    term_file = 'test/files/{}.csv'.format(TERM)
    N = 3

    termline = parse_term(term_file, N)

    w1 = (1+math.log10(4))*math.log10(N/2)
    w2 = (1+math.log10(2))*math.log10(N/2)

    eq_(termline,
        '598859a0-eaa7-466a-8919-e6260c89edef:{},'
        '31a8e3b4-8c67-4fb7-b11a-1df1105617a2:{}'.format(w1, w2))


TEST_DICT_PATH = DATA_DIR + 'testdict.dat'
TEST_INDEXINFO_PATH = DATA_DIR + 'testinfo.dat'


def clean_testfiles():
    for f in [TEST_DICT_PATH, TEST_INDEXINFO_PATH]:
        try:
            os.remove(TEST_DICT_PATH)
        except FileNotFoundError:
            pass


@with_setup(clean_testfiles, clean_testfiles)
@mock.patch('tsg.indexer.base.create_indexinfo')
def test_create_index(create_indexinfo_mock):
    import ipdb
    ipdb.set_trace()
    num_documents = 3
    # TODO add some files to test/files/intermediate and check the dictionary
    # later
    create_index('test/files/intermediate/',
                 num_documents,
                 TEST_DICT_PATH,
                 TEST_INDEXINFO_PATH)

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
    pass
