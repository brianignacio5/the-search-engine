import math
import numpy as np
import json
import operator
import re

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

        for uuid, weight in re.findall('(?:,|^)(.*?):([0-9]+\.[0-9]*)',
                                      documents):
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

def and_score_calc(query_terms, index_dictionary_path= DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):

    common__doc_keys = set()
    terms_documents = {}
    and_scored_docs = {}
    doc_length = {}
    query_length = {}

    for term in query_terms:
        terms_documents[term] = get_dictionary_term_list(term, index_dictionary_path)
        if len(common__doc_keys) == 0:
            common__doc_keys = terms_documents[term].keys()
        else:
            common__doc_keys &= terms_documents[term].keys()

    for key in common__doc_keys:
        for term in query_terms:
            if key in terms_documents[term]:
                query_term_weight = calculate_query_term_weight(term,query_terms,
            index_dictionary_path, index_info_path)
                if key in and_scored_docs:
                    and_scored_docs[key] += float(terms_documents[term][key])*float(query_term_weight)
                else:
                    and_scored_docs[key] = float(terms_documents[term][key])*float(query_term_weight)

                if key in doc_length:
                    doc_length[key] += math.pow(float(terms_documents[term][key]), float(2))
                    query_length[key] += math.pow(float(query_term_weight), float(2))
                else:
                    doc_length[key] = math.pow(float(terms_documents[term][key]), float(2))
                    query_length[key] = math.pow(float(query_term_weight), float(2))

    for key in and_scored_docs:
        try:
            and_scored_docs[key] = and_scored_docs[key] / (math.sqrt(doc_length[key])*math.sqrt(query_length[key]))
        except ZeroDivisionError:
            and_scored_docs[key] = 0

    return and_scored_docs

def or_score_calc(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH):

    or_scored_docs = {}
    query_length = {} # Holds score^2 for Length normalization at end
    doc_length = {}
    for term in query_terms:
        query_term_weight = calculate_query_term_weight(term,query_terms,
            index_dictionary_path, index_info_path)
        term_documents = get_dictionary_term_list(term, index_dictionary_path)
        for key, value in term_documents.items():
            if key in or_scored_docs:
                or_scored_docs[key] += float(value)*float(query_term_weight)
            else:
                or_scored_docs[key] = float(value)*float(query_term_weight)

            if key in query_length:
                query_length[key] += math.pow(float(query_term_weight), float(2))
                doc_length[key] += math.pow(float(value),float(2))
            else:
                query_length[key] = math.pow(float(query_term_weight), float(2))
                doc_length[key] = math.pow(float(value), float(2))

    for key in or_scored_docs:
        try:
            or_scored_docs[key] = or_scored_docs[key] / (math.sqrt(query_length[key])*math.sqrt(doc_length[key]))
        except ZeroDivisionError:
            or_scored_docs[key] = 0

    return or_scored_docs

def combine_and_or_scores(and_dict, or_dict):
    or_docs_not_in_and_docs = {}

    for key, value in or_dict.items():
        if key not in and_dict.keys():
            or_docs_not_in_and_docs[key] = value

    sorted_and = sorted(and_dict.items(), key = operator.itemgetter(1,0), reverse = True)
    sorted_or = sorted(or_docs_not_in_and_docs.items(), key= operator.itemgetter(1,0), reverse= True)

    combined_and_or_docs = sorted_and + sorted_or

    return combined_and_or_docs

def rank(query_terms, index_dictionary_path=DICTIONARY_PATH,
    index_info_path = INDEXINFO_PATH, rank_method = "and_or_extended"):
    '''
    Ranker takes a query and a dictionary path to calculates the score
    and retrieved a list of docs ordered by score and doc_id as
    tuples [(doc_1,score_1),(doc_2, score_2), ..., (doc_n,score_n)]
    '''
    and_scored_docs = {}
    or_scored_docs = {}
    sorted_docs = []

    if rank_method == "and":
        and_scored_docs = and_score_calc(query_terms, index_dictionary_path, index_info_path)
        sorted_docs = sorted(and_scored_docs.items(), key = operator.itemgetter(1), reverse = True)
    elif rank_method == "or":
        or_scored_docs = or_score_calc(query_terms, index_dictionary_path, index_info_path)
        sorted_docs = sorted(or_scored_docs.items(), key = operator.itemgetter(1), reverse = True)
    elif rank_method == "and_or_extended":
        and_scored_docs = and_score_calc(query_terms, index_dictionary_path, index_info_path)
        or_scored_docs = or_score_calc(query_terms, index_dictionary_path, index_info_path)
        sorted_docs = combine_and_or_scores(and_scored_docs, or_scored_docs)

    return sorted_docs
