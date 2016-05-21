import os
import operator
import tsg.ranker as ranker 

RAW_TEST_DIRECTORY = os.path.dirname(__file__) + "/files/ranker/"
TEST_DICT_PATH = RAW_TEST_DIRECTORY + 'testdict.dat'
TEST_DICT_PATH2 = RAW_TEST_DIRECTORY + 'testdict2.dat'

def test_extract_termfile():

    term = 'term'
    term_list = ranker.get_dictionary_term_list(term,TEST_DICT_PATH)

    assert len(term_list) > 0
    assert term_list == {"7dd5a186-1dfe-4be6-be0b-ded65e8067c9": 1.0,
                         "c7c1d354-4b85-438b-bb2e-89350e40e33f": 1.1760912590557,
                         "15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0": 1.0}

    term = 'oblivion'
    term_list = ranker.get_dictionary_term_list(term,TEST_DICT_PATH)

    assert len(term_list) == 0

def test_and_score_calc():
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = {'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.0, 
              '7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.0}

    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH)

    assert scored_docs_by_function == scored_docs

    query_terms = ['oblivion']
    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH)
    assert len(scored_docs_by_function) == 0

def test_and_score_calc2():
    query_terms = ['morrisett', '2712791']

    scored_docs = {'author_s_Salem=Silva:Francisco': 1.0, 
                   'author_l_Lemus=Rodr=iacute=guez:Enrique': 0.2537600495952614}

    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH2)

    assert scored_docs_by_function == scored_docs

    query_terms = ['oblivion']
    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH2)
    assert len(scored_docs_by_function) == 0

def test_or_score_calc():
    
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = {'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.0, 
                   'c7c1d354-4b85-438b-bb2e-89350e40e33f': 0.7840608393704667, 
                   '7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.0}

    scored_docs_by_function = ranker.or_score_calc(query_terms, TEST_DICT_PATH)
    assert scored_docs_by_function == scored_docs

def test_or_score_calc2():
    
    query_terms = ['morrisett', '2712791']

    scored_docs = {'journal_jam_jam2013': 1.0, 
                   'conference_ijcnn_ijcnn2006': 0.3652509614113979, 
                   'author_k_Krishnamurthi:Shriram': 0.054977984172906724}

    scored_docs_by_function = ranker.or_score_calc(query_terms, TEST_DICT_PATH2)
    
    for key, value in scored_docs.items():
        assert scored_docs_by_function[key] == scored_docs[key]

def test_combine_and_or_scores():
    and_scores = {'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 0.9998169851514684, 
              '7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 0.9997654994406655}

    or_scores = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 0.9997654994406655, 
              'c7c1d354-4b85-438b-bb2e-89350e40e33f': 0.9999984674316662, 
              '15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 0.9998169851514684}

    scored_docs = [('15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0', 0.9998169851514684), 
                   ('7dd5a186-1dfe-4be6-be0b-ded65e8067c9', 0.9997654994406655), 
                   ('c7c1d354-4b85-438b-bb2e-89350e40e33f', 0.9999984674316662)]

    scored_docs_by_function = ranker.combine_and_or_scores(and_scores, or_scores)
    
    assert scored_docs_by_function == scored_docs

def test_rank():
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.0, 
                   '15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.0,
                   'c7c1d354-4b85-438b-bb2e-89350e40e33f': 0.7840608393704667}

    scored_docs = sorted(scored_docs.items(), key = operator.itemgetter(1), reverse = True)

    scored_docs_by_function = ranker.rank(query_terms, TEST_DICT_PATH,
        "and_or_extended")

    assert scored_docs_by_function == scored_docs

def test_rank2():
    query_terms = ['morrisett','2712791']

    scored_docs = {'author_s_Salem=Silva:Francisco': 1.0, 
                   'author_l_Lemus=Rodr=iacute=guez:Enrique': 0.2537600495952614,
                   'journal_jam_jam2013': 1.0,
                   'conference_ijcnn_ijcnn2006': 0.3652509614113979}

    scored_docs = sorted(scored_docs.items(), key = operator.itemgetter(1), reverse = True)

    scored_docs_by_function = ranker.rank(query_terms, TEST_DICT_PATH2,
        "and_or_extended")

    for score in scored_docs:
               assert score in scored_docs_by_function
       