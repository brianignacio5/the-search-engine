import math
import os, os.path
from collections import defaultdict
import numpy as np
from tsg.config import DICTIONARY_PATH, RAW_DIR

def get_dictionary_term_list(term,dictionary=DICTIONARY_PATH) :
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
	term_dictionary = get_dictionary_term_list(term, dictionary)
	N = len([name for name in os.listdir(RAW_DIR) if os.path.isfile(os.path.join(RAW_DIR,name))])
	doc_freq = len(term_dictionary)
	term_freq = query.lower().count(term)
	weight = (1+ np.log10(term_freq))*math.log10(N/doc_freq)

	return weight

def cosine_score_calc(query,dictionary=DICTIONARY_PATH): 
	query_terms = query.split('')

	Scores = defaultdict(float)
	Length = defaultdict(float) # Holds numbers of docs for each term

	for term in query_terms:
		query_term_weight = calculate_query_term_weight(term,query,dictionary)
		term_list = get_dictionary_term_list(term,dictionary)
		for key, value in term_list.items():
			Scores[key] += value*query_term_weight
			Length[key] += math.pow(float(Scores[key]),float(2))

	for i, score in enumerate(Scores):
		Scores[i] = score / Length[i]

	return Scores