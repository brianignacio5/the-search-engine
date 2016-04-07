import math
import numpy as np
import os
from tsg.config import DATA_DIR, RAW_DIR
from tsg.ranker import get_dictionary_term_list, cosine_score_calc, calculate_query_term_weight

def mock_dictionary_create() :
	line1 = 'term c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3322237271982384,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
	line2 = 'to c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3322237271982384,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3205763030575843\n'
	line3 = 'evaluate c7c1d354-4b85-438b-bb2e-89350e40e33f:3.3205763030575843,15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0:3.3205763030575843,7dd5a186-1dfe-4be6-be0b-ded65e8067c9:3.3322237271982384\n'
	mock_filename = DATA_DIR + 'mock_dictionary.dat'

	with open(mock_filename,'w') as f:
		f.write(line1)
		f.write(line2)
		f.write(line3)

def test_extract_termfile() :

	term = 'term'
	mock_filename = DATA_DIR + 'mock_dictionary.dat'
	try:
		os.remove(mock_filename)
	except OSError:
		pass
	assert not os.path.exists(mock_filename)
	mock_dictionary_create()

	term_list = { }
	term_list = get_dictionary_term_list(term,mock_filename)

	assert len(term_list) > 0
	print(term_list)
	assert term_list == {"7dd5a186-1dfe-4be6-be0b-ded65e8067c9": "3.3205763030575843",
						 "c7c1d354-4b85-438b-bb2e-89350e40e33f": "3.3322237271982384",
						 "15da4df3-9ef1-4e1a-b0ba-f93bf05a25d0": "3.3205763030575843"}

def test_term_query_weight() :
	query = 'term to evaluate'
	mock_filename = DATA_DIR + 'mock_dictionary.dat'
	try:
		os.remove(mock_filename)
	except OSError:
		pass
	assert not os.path.exists(mock_filename)
	mock_dictionary_create()

	term_freq = query.count('term')
	doc_freq = 3 #Check mock dictionary
	term_weight = calculate_query_term_weight('term',query,mock_filename)

	#N is number of docs in collection
	N = len([name for name in os.listdir(RAW_DIR) if os.path.isfile(os.path.join(RAW_DIR,name))])
	weight = (1+ np.log10(term_freq))*math.log10(N/doc_freq)
	assert term_weight == weight

def test_cosine_score_calc() :

	query = 'term to evaluate'
	mock_filename = DATA_DIR + 'mock_dictionary.dat'
	try:
		os.remove(mock_filename)
	except OSError:
		pass
	assert not os.path.exists(mock_filename)
	mock_dictionary_create()

	parts = query.split(' ')
	term1 = parts[0]
	term1_list = get_dictionary_term_list(term1, mock_filename)
	term1_query_weight = calculate_query_term_weight(term1,query,mock_filename)

	term2 = parts[1]
	term2_list = get_dictionary_term_list(term2, mock_filename)
	term2_query_weight = calculate_query_term_weight(term2,query,mock_filename)

	term3 = parts[2]
	term3_list = get_dictionary_term_list(term3, mock_filename)
	term3_query_weight = calculate_query_term_weight(term3,query,mock_filename)

	Score = { } # Holds tf-idf value for each doc- query term pair
	Length = { } # Holds numbers of docs for each term

	for key,value in term1_list.items():
		if key in Score:
			Score[key] += float(value)*float(term1_query_weight)
		else:
			Score[key] = float(value)*float(term1_query_weight)

		if key in Length:
			Length[key] += math.pow(float(Score[key]),float(2))
		else:
			Length[key] = math.pow(float(Score[key]),float(2))

	for key,value in term2_list.items():
		if key in Score:
			Score[key] += float(value)*float(term2_query_weight)
		else:
			Score[key] = float(value)*float(term2_query_weight)

		if key in Length:
			Length[key] += math.pow(float(Score[key]),float(2))
		else:
			Length[key] = math.pow(float(Score[key]),float(2))

	for key,value in term3_list.items():
		if key in Score:
			Score[key] += float(value)*float(term3_query_weight)
		else:
			Score[key] = float(value)*float(term3_query_weight)

		if key in Length:
			Length[key] += math.pow(float(Score[key]),float(2))
		else:
			Length[key] = math.pow(float(Score[key]),float(2))

	for key in Score:
		Score[key] = Score[key] / Length[key]

	Score_by_function = cosine_score_calc(query, mock_filename)

	assert Score_by_function == Score

