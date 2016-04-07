from mock import patch

from tsg.search import search

@patch('tsg.parser.parse_text')
@patch('tsg.ranker.parse_text')
def test_search():
    # should call (query)parser
    # should call ranker
    # should return list
    # scores should be sorted
