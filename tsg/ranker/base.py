import math
import os, os.path
import numpy as np
from tsg.config import DICTIONARY_PATH, RAW_DIR

def get_dictionary_term_list(term) :
	term_list = []
	with open(DICTIONARY_PATH) as dict_f:
		for line in dict_f:
			if term in line:
				parts = line[len(term)+1:].split(term).split(',')
				term_list = []
				for doc_data in parts:
					doc_data_parts = parts.split(':')
					term_list[doc_data_parts[0]] = doc_data_parts[1]
	return term_list

def calculate_query_term_weight(term,query):
	term_dictionary = get_dictionary_term_list(term)
	N = len([name for name in os.listdir(RAW_DIR) if os.path.isfile(name)])
	doc_freq = len(term_dictionary)
	term_freq = query.lower().count(term)
	weight = (1+ np.log10(term_freq))*math.log10(N/doc_freq)

	return weight

def cosine_score_calc(query): 
	term_lists = { }
	query_terms = query.split('')
	for term in query_terms:
		term_list = get_dictionary_term_list(term)
		term_lists = [term_lists, term_list]

	Scores = []
	Length = [] # Holds numbers of docs for each term

	for term in query_terms:
		query_term_weight = calculate_query_term_weight(term,query)
		term_list = get_dictionary_term_list(term)
		for key in term_list:
			Scores[key] += term_list[key]*query_term_weight
			Length[key] += math.pow(Scores[key],2)

	for i, score in enumerate(Scores):
		Scores[i] = score / Length[i]

	return Scores