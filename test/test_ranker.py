from nose.tools import eq_
from nose import with_setup
import math
import os
import json
from tsg.config import DATA_DIR
from tsg.ranker import get_dictionary_term_list, cosine_score_calc, calculate_query_term_weight, get_number_of_docs

TEST_DICT_PATH = DATA_DIR + 'testdict.dat'
TEST_INDEXINFO_PATH = DATA_DIR + 'testinfo.json'

def create_dictionary_index():
    line1 = 'term c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3322237271982384,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
    line2 = 'to c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3322237271982384,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
    line3 = 'evaluate c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3322237271982384\n'

    with open(TEST_DICT_PATH,'w') as dict_f:
        dict_f.write(line1)
        dict_f.write(line2)
        dict_f.write(line3)

    num_docs = 25813

    obj = {"num_documents": num_docs}
    with open(TEST_INDEXINFO_PATH, 'w') as f:
        json.dump(obj, f)

def remove_test_dict_info():
    try:
        os.remove(TEST_DICT_PATH)
        os.remove(TEST_INDEXINFO_PATH)
    except OSError:
        pass
    assert not os.path.exists(TEST_DICT_PATH)
    assert not os.path.exists(TEST_INDEXINFO_PATH)


@with_setup(create_dictionary_index,remove_test_dict_info)
def test_extract_termfile():

    term = 'term'
    term_list = get_dictionary_term_list(term,TEST_DICT_PATH)

    assert len(term_list) > 0
    assert term_list == {"7dd5a186-1dfe-4be6-be0b-ded65e8067c9": "3.3205763030575843",
                         "c7c1d354-4b85-438b-bb2e-89350e40e33f": "3.3322237271982384",
                         "15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0": "3.3205763030575843"}

@with_setup(create_dictionary_index,remove_test_dict_info)
def test_get_number_docs():
    N = get_number_of_docs(TEST_INDEXINFO_PATH)
    assert N == 25813

@with_setup(create_dictionary_index,remove_test_dict_info)
def test_term_query_weight():
    N = get_number_of_docs(TEST_INDEXINFO_PATH)
    weight = math.log10(N/3)

    query = 'term to evaluate'
    term_weight = calculate_query_term_weight('term',query,TEST_DICT_PATH, TEST_INDEXINFO_PATH)

    eq_(round(term_weight,4), round(weight,4))

@with_setup(create_dictionary_index,remove_test_dict_info)
def test_cosine_score_calc():
    query = 'term to evaluate'

    scores = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.7320484452685714,
                    '15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.7320484452685714,
                    'c7c1d354-4b85-438b-bb2e-89350e40e33f': 1.7320484452685714}

    scores_by_function = cosine_score_calc(query, TEST_DICT_PATH, TEST_INDEXINFO_PATH)
    
    assert scores_by_function == scores
