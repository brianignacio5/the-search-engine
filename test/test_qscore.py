from tsg.indexer import qscore
from nose.tools import eq_


def test_get_scores():
    parsed_test_dir = 'test/files/parsed'
    qscores = qscore.get_scores(parsed_test_dir)

    eq_(qscores['first'], 2/3)
    eq_(qscores['second'], 2/3)
    eq_(qscores['third'], 0.71955175131048577)
    eq_(qscores['fourth'], 0.94711491535618098)

def test_normalized_quality_score():
    mean = 2
    std = 2
    value = 6
    eq_(qscore._normalized_quality_score(mean, std, value), 0.99241662268394026)

    # std == 0
    eq_(qscore._normalized_quality_score(1, 0, 2), 1)
    eq_(qscore._normalized_quality_score(1, 0, 3), 1)
    eq_(qscore._normalized_quality_score(1, 0, 0), 2/3)
    eq_(qscore._normalized_quality_score(3, 0, 0), 2/3)
