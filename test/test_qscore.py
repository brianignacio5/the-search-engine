from tsg.intermediate import qscore
from nose.tools import eq_


def test_get_distributions():
    parsed_test_dir = 'test/files/parsed'
    distributions = qscore.get_distributions(parsed_test_dir)

    eq_(distributions['conference'], (1.0, 0.0))
    eq_(distributions['conference_overview'], (2.0 ,2.0))
    eq_(distributions['author'], (3.0, 0.0))
