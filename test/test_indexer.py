from nose.tools import eq_
import math

from tsg.indexer import parse_term, hash_index


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


def test_hash_index():
    hash_index()
    pass
