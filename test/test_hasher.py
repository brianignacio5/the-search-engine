from nose.tools import eq_
from tsg.ranker.hasher import hash_index_terms

TEST_DICT_FILENAME = 'test/files/test_dict.dat'


def test_hash_index_terms():
    position_hash = hash_index_terms(TEST_DICT_FILENAME)
    eq_(position_hash, {
        'term': (0, 3),
        'to': (173, 3),
        'evaluate': (344, 3)
    })
