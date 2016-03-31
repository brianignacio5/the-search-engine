import math

from tsg.config import DICTIONARY_PATH
from tsg.ranker import get_dictionary_term_list, Cosine_score_calc

def test_extract_termfile() :

	term = 'Term to evaluate'
	term_list = get_dictionary_term_list(term)

	#Get Dict term list
	term_list = {}
	with open(DICTIONARY_PATH) as dict_f:
		for line in dict_f:
			if term in line:
				parts = line.split(term).split(',')
				for doc_data in parts:
					doc_data_parts = parts.split(':')
					term_list[doc_data_parts[0]] = doc_data_parts[1]

	assert len(term_list) > 0

	assert term_list[1] == {"doc1":"tf-idf","doc2": "tf-idf"}

def test_cosine_score_calc() :

	query = 'Query to search'
	parts = query.split(' ')
	term1 = parts[0]
	term1_list = get_dictionary_term_list(term)

	term2 = parts[1]
	term2_list = get_dictionary_term_list(term)
	Score = [] # Holds tf-idf value for each doc- query term pair
	Length = [] # Holds numbers of docs for each term

	for term in query_terms:
		query_term_weight = calculate_query_term_weight(term,query)
		term_list = get_dictionary_term_list(term)
		for doc in term_list:
			Score[doc_Id] += get_tf_idf_score(doc)*query_term_weight
			Length[doc_Id] += math.pow(Score[doc_Id],2)

	for i, score in enumerate(Score):
		Score[i] = score / Length[i]
	
	Docs_assert = get_docs_by_score(Score)

	Docs_results = Cosine_score_calc(query)

	assert Docs_results[:2] == Docs_assert[:2]

