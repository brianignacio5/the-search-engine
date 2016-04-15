import math
import numpy as np
import json
import operator
from tsg.config import DICTIONARY_PATH, INDEXINFO_PATH


def get_dictionary_term_list(term,index_dictionary_path=DICTIONARY_PATH) :

    # TODO Modify dictionary to use a position instead of reading
    # the whole dictionary. Use file.seek(position, 0) and get
    # position from dictionary hash.

    term_list = { }
    with open(index_dictionary_path) as dict_f:
        for line in dict_f:
            line_term, documents = line.split(' ')

            if term == line_term:
                parts = documents.split(',')
                for doc_data in parts:
                    doc_data_parts = doc_data.split(':')
                    term_list[doc_data_parts[0]] = float(doc_data_parts[1].replace("\n",""))
    return term_list

def get_number_of_docs(index_dictionary_path):
    dict_f = { }
    with open(index_dictionary_path) as info:
        dict_f = json.load(info)

    return dict_f["num_documents"]


def calculate_query_term_weight(term, query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):
    term_dictionary = get_dictionary_term_list(term, index_dictionary_path)
    N = get_number_of_docs(index_info_path)
    doc_freq = len(term_dictionary)
    term_freq = query_terms.count(term)
    try:
        weight = (1+ np.log10(term_freq))*math.log10(N/doc_freq)
    except ZeroDivisionError:
        weight = 0

    return weight

def cosine_score_calc(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):

    scores = { }
    length = { } # Holds score^2 for Length normalization at end

    for term in query_terms:
        query_term_weight = calculate_query_term_weight(term,query_terms,
            index_dictionary_path, index_info_path)
        term_list = get_dictionary_term_list(term, index_dictionary_path)
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

def rank(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):
    '''
    Ranker takes a query and a dictionary path to calculates the score
    and retrieved a list of docs ordered by score and doc_id as
    tuples [(doc_1,score_1),(doc_2, score_2), ..., (doc_n,score_n)]
    '''
    cosine_scores = cosine_score_calc(query_terms, index_dictionary_path, index_info_path)

    # TODO Add PageRank scores
    # loop: for each key (docID) add pagerank(docId) score

    # Sort by score value then doc_id, in case of equal score docs.
    sorted_docs = sorted(cosine_scores.items(), key = operator.itemgetter(1,0))

    return sorted_docs
