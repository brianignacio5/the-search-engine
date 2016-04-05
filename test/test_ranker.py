import math

from tsg.config import DICTIONARY_PATH
from tsg.ranker import get_dictionary_term_list, cosine_score_calc, calculate_query_term_weight

def test_extract_termfile() :

	term = 'Term to evaluate'
	term_list = get_dictionary_term_list(term)

	#Get Dict term list
	term_list = {}
	with open(DICTIONARY_PATH) as dict_f:
		for line in dict_f:
			if term in line:
				parts = line[len(term)+1:].split(term).split(',')
				for doc_data in parts:
					doc_data_parts = parts.split(':')
					term_list[doc_data_parts[0]] = doc_data_parts[1]

	assert len(term_list) > 0

	assert term_list[1] == {"doc1":"tf-idf","doc2": "tf-idf"}

def test_cosine_score_calc() :

	query = 'Query to search'
	parts = query.split(' ')
	term1 = parts[0]
	term1_list = get_dictionary_term_list(term1)

	term2 = parts[1]
	term2_list = get_dictionary_term_list(term2)
	Score = [] # Holds tf-idf value for each doc- query term pair
	Length = [] # Holds numbers of docs for each term

	for term in parts:
		query_term_weight = calculate_query_term_weight(term,query)
		term_list = [term1_list,term2_list]
		for key in term_list:
			Score[key] += term_list[key]*query_term_weight
			Length[key] += math.pow(Score[key],2)

	for i, score in enumerate(Score):
		Score[i] = score / Length[i]
	
	Docs_assert = cosine_score_calc(Score)

	Docs_results = cosine_score_calc(query)

	assert Docs_results[:2] == Docs_assert[:2]

