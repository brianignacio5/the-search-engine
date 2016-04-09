import math
import glob
import numpy as np
import operator
from tsg.config import DICTIONARY_PATH, RAW_DIR

def get_dictionary_term_list(term,dictionary=DICTIONARY_PATH) :

	# TODO Modify dictionary to use a position instead of reading
	# the whole dictionary. Use file.seek(position, 0) and get
	# position from dictionary hash.

	term_list = { }
	with open(dictionary) as dict_f:
		for line in dict_f:
			if term in line:
				parts = line[len(term)+1:].split(',')
				for doc_data in parts:
					doc_data_parts = doc_data.split(':')
					term_list[doc_data_parts[0]] = doc_data_parts[1].replace("\n","")
	return term_list

def calculate_query_term_weight(term, query, dictionary=DICTIONARY_PATH):

	# TODO Pass the path of dictionary and dictionary hash to get_dictionary_term_list

	term_dictionary = get_dictionary_term_list(term, dictionary)
	N = len(glob.glob(RAW_DIR+'*.html'))
	doc_freq = len(term_dictionary)
	term_freq = query.lower().count(term)
	weight = (1+ np.log10(term_freq))*math.log10(N/doc_freq)

	return weight

def cosine_score_calc(query,dictionary=DICTIONARY_PATH): 

	# TODO Pass the path of dictionary and dictionary hash to get_dictionary_term_list

	query_terms = query.split(' ')

	scores = { }
	length = { } # Holds score^2 for Length normalization at end

	for term in query_terms:
		query_term_weight = calculate_query_term_weight(term,query,dictionary)
		term_list = get_dictionary_term_list(term,dictionary)
		for key, value in term_list.items():
			if key in scores:
				scores[key] += float(value)*float(query_term_weight)
			else:
				scores[key] = float(value)*float(query_term_weight)

			if key in length:
				length[key] += math.pow(float(value)*float(query_term_weight),float(2))
			else:
				length[key] = math.pow(float(value)*float(query_term_weight),float(2))

	for key in scores:
		scores[key] = scores[key] / math.sqrt(length[key])

	return scores

def rank(query,index_directory):
	'''
	Ranker takes a query and a dictionary path to calculates the score
	and retrieved a list of docs ordered by score and doc_id as
	tuples [(doc_1,score_1),(doc_2, score_2), ..., (doc_n,score_n)] 
	'''

	# TODO Pass the path of dictionary and dictionary hash to get_dictionary_term_list

	cosine_scores = cosine_score_calc(query,index_directory)

	# TODO Add PageRank scores
	# loop: for each key (docID) add pagerank(docId) score

	# Sort by score value then doc_id, in case of equal score docs.
	sorted_docs = sorted(cosine_scores.items(), key = operator.itemgetter(1,0))

	return sorted_docs