import math
import numpy as np
import json
import operator

from tsg.config import DICTIONARY_PATH, INDEXINFO_PATH
from tsg.ranker.hasher import hash_index_terms


def get_dictionary_term_list(term,index_dictionary_path=DICTIONARY_PATH):

    if not get_dictionary_term_list.index_hash:
        get_dictionary_term_list.index_hash = hash_index_terms(index_dictionary_path)

    document_list = {}
    with open(index_dictionary_path) as dict_f:
        dict_f.seek(get_dictionary_term_list.index_hash[term][0])
        line_term, documents = dict_f.readline().replace('\n', '').split(' ')

        assert term == line_term

        for doc_data in documents.split(','):
            uuid, weight = doc_data.split(':')
            document_list[uuid] = float(weight)

    return document_list
get_dictionary_term_list.index_hash = None

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

def conjunctive_score_calc(query_terms, index_dictionary_path= DICTIONARY_PATH, 
    index_info_path = INDEXINFO_PATH):
    
    results_keys = set()
    terms_lists = {}
    scores = {}
    doc_length = {}
    query_length = {}

    for term in query_terms:
        terms_lists[term] = get_dictionary_term_list(term, index_dictionary_path)
        if len(results_keys) == 0:
            results_keys = terms_lists[term].keys()
        else:
            results_keys &= terms_lists[term].keys()

    for key in results_keys:
        for term in query_terms:
            if key in terms_lists[term].keys():
                query_term_weight = calculate_query_term_weight(term,query_terms,
            index_dictionary_path, index_info_path)
                if key in scores:
                    scores[key] += float(terms_lists[term][key])*float(query_term_weight)
                else:
                    scores[key] = float(terms_lists[term][key])*float(query_term_weight)

                if key in doc_length:
                    doc_length[key] += math.pow(float(terms_lists[term][key]), float(2))
                    query_length[key] += math.pow(float(query_term_weight), float(2))
                else:
                    doc_length[key] = math.pow(float(terms_lists[term][key]), float(2))
                    query_length[key] = math.pow(float(query_term_weight), float(2))

    for key in scores:
        try:
            scores[key] = scores[key] / (math.sqrt(doc_length[key])*math.sqrt(query_length[key]))
        except ZeroDivisionError:
            scores[key] = 0

    return scores

def cosine_score_calc(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):

    scores = {}
    query_length = {} # Holds score^2 for Length normalization at end
    doc_length = {}
    for term in query_terms:
        query_term_weight = calculate_query_term_weight(term,query_terms,
            index_dictionary_path, index_info_path)
        term_list = get_dictionary_term_list(term, index_dictionary_path)
        for key, value in term_list.items():
            if key in scores:
                scores[key] += float(value)*float(query_term_weight)
            else:
                scores[key] = float(value)*float(query_term_weight)

            if key in query_length:
                query_length[key] += math.pow(float(query_term_weight), float(2))
                doc_length[key] += math.pow(float(value),float(2))
            else:
                query_length[key] = math.pow(float(query_term_weight), float(2))
                doc_length[key] = math.pow(float(value), float(2))

    for key in scores:
        try:
            scores[key] = scores[key] / (math.sqrt(query_length[key])*math.sqrt(doc_length[key]))
        except ZeroDivisionError:
            scores[key] = 0

    return scores

def combine_and_or_scores(and_dict, or_dict):
    sorted_and = sorted(and_dict.items(), key = operator.itemgetter(1,0))
    sorted_or = sorted(or_dict.items(), key = operator.itemgetter(1, 0))

    new_docs = set(sorted_or) - set(sorted_and)

    scores = sorted_and + list(new_docs)

    return scores

def rank(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):
    '''
    Ranker takes a query and a dictionary path to calculates the score
    and retrieved a list of docs ordered by score and doc_id as
    tuples [(doc_1,score_1),(doc_2, score_2), ..., (doc_n,score_n)]
    '''
    and_scores = conjunctive_score_calc(query_terms, index_dictionary_path, index_info_path)
    or_scores = cosine_score_calc(query_terms, index_dictionary_path, index_info_path)

    # TODO Add PageRank scores
    # loop: for each key (docID) add pagerank(docId) score

    sorted_docs = combine_and_or_scores(and_scores, or_scores)

    return sorted_docs
