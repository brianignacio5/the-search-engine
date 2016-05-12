from nose import with_setup
import os
import json
from tsg.config import DATA_DIR
import tsg.ranker as ranker 

TEST_DICT_PATH = DATA_DIR + 'testdict.dat'
TEST_INDEXINFO_PATH = DATA_DIR + 'testinfo.json'

def create_dictionary_index():
    line1 = 'term c7c1d354-4b85-438b-bb2e-89350e40e33f:1.1760912590557,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:1.0,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:1.0\n'
    line2 = 'to 15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:1.0,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:1.0\n'
    line3 = 'evaluate c7c1d354-4b85-438b-bb2e-89350e40e33f:1.1760912590557,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:1.0,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:1.0\n'

    with open(TEST_DICT_PATH,'w') as dict_f:
        dict_f.write(line1)
        dict_f.write(line2)
        dict_f.write(line3)

    num_docs = 3

    obj = {"num_documents": num_docs}
    with open(TEST_INDEXINFO_PATH, 'w') as f:
        json.dump(obj, f)

def remove_test_dict_info():
    try:
        os.remove(TEST_DICT_PATH)
    except OSError:
        pass

    try:
        os.remove(TEST_INDEXINFO_PATH)
    except OSError:
        pass
    assert not os.path.exists(TEST_DICT_PATH)
    assert not os.path.exists(TEST_INDEXINFO_PATH)


@with_setup(create_dictionary_index,remove_test_dict_info)
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

@with_setup(create_dictionary_index, remove_test_dict_info)
def test_and_score_calc():
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = {'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.0, 
              '7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.0}

    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH, 
        TEST_INDEXINFO_PATH)

    assert scored_docs_by_function == scored_docs

    query_terms = ['oblivion']
    scored_docs_by_function = ranker.and_score_calc(query_terms, TEST_DICT_PATH, 
        TEST_INDEXINFO_PATH)
    assert len(scored_docs_by_function) == 0

@with_setup(create_dictionary_index,remove_test_dict_info)
def test_or_score_calc():
    
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.0, 
              'c7c1d354-4b85-438b-bb2e-89350e40e33f': 0.850274153727589, 
              '15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.0}

    scored_docs_by_function = ranker.or_score_calc(query_terms, TEST_DICT_PATH, 
        TEST_INDEXINFO_PATH)

    assert scored_docs_by_function == scored_docs

@with_setup(create_dictionary_index,remove_test_dict_info)
def test_combine_and_or_scores():
    and_scores = {'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 0.9998169851514684, 
              '7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 0.9997654994406655}

    or_scores = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 0.9997654994406655, 
              'c7c1d354-4b85-438b-bb2e-89350e40e33f': 0.9999984674316662, 
              '15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 0.9998169851514684}

    scored_docs = [('7dd5a186-1dfe-4be6-be0b-ded65e8067c9', 0.9997654994406655),
                   ('15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0', 0.9998169851514684),
                   ('c7c1d354-4b85-438b-bb2e-89350e40e33f', 0.9999984674316662)]

    scored_docs_by_function = ranker.combine_and_or_scores(and_scores, or_scores)

    assert scored_docs_by_function == scored_docs


@with_setup(create_dictionary_index,remove_test_dict_info)
def test_rank():
    #query = 'term to evaluate'
    query_terms = ['term', 'to', 'evaluate']

    scored_docs = sorted([('7dd5a186-1dfe-4be6-be0b-ded65e8067c9', 1.0), 
              ('15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0', 1.0),
              ('c7c1d354-4b85-438b-bb2e-89350e40e33f', 0.850274153727589)])

    scored_docs_by_function = ranker.rank(query_terms, TEST_DICT_PATH,
        TEST_INDEXINFO_PATH, "and_or_extended")

    assert scored_docs_by_function == scored_docs
