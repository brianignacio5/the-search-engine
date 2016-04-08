from mock import patch

from tsg.search import search

@patch('tsg.parser.parse_text')
def test_search(parse_text_mock):
    #search()
    # should call (query)parser
    # should call ranker
    # should return list
    # scores should be sorted
    pass
