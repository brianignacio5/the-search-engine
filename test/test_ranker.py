import os
from tsg.config import DATA_DIR
from tsg.ranker import get_dictionary_term_list, cosine_score_calc, calculate_query_term_weight

def mock_dictionary_create() :
	line1 = 'term c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3322237271982384,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
	line2 = 'to c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3322237271982384,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
	line3 = 'evaluate c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3322237271982384\n'

	try:
		os.remove(mock_filename)
	except OSError:
		pass
	assert not os.path.exists(mock_filename)

	with open(mock_filename,'w') as f:
		f.write(line1)
		f.write(line2)
		f.write(line3)

mock_filename = DATA_DIR + 'mock_dictionary.dat'
mock_dictionary_create()

def test_extract_termfile() :

	term = 'term'
	term_list = get_dictionary_term_list(term,mock_filename)

	assert len(term_list) > 0
	assert term_list == {"7dd5a186-1dfe-4be6-be0b-ded65e8067c9": "3.3205763030575843",
						 "c7c1d354-4b85-438b-bb2e-89350e40e33f": "3.3322237271982384",
						 "15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0": "3.3205763030575843"}

def test_term_query_weight() :

	weight = 3.69885417703

	query = 'term to evaluate'
	term_weight = calculate_query_term_weight('term',query,mock_filename)

	assert round(term_weight,4) == round(weight,4)

def test_cosine_score_calc() :

	query = 'term to evaluate'

	scores = {'7dd5a186-1dfe-4be6-be0b-ded65e8067c9': 1.7320484452685714, 
					'15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0': 1.7320484452685714, 
					'c7c1d354-4b85-438b-bb2e-89350e40e33f': 1.7320484452685714}

	scores_by_function = cosine_score_calc(query, mock_filename)

	assert scores_by_function == scores

