import json

from tsg.config import PARSED_DIR
from tsg.parser import parse_text


def _generate_detailed_item(doc_id, doc_weight, search_terms):
    with open('{}{}.json'.format(PARSED_DIR, doc_id)) as doc_file:
        detailed_data = json.load(doc_file)
        content = detailed_data['content']

        # generate a content preview
        term_pos = content.find(' {} '.format(search_terms[0]))+1
        preview = '{}<b>{}</b>{}'.format(
            content[term_pos-100:term_pos], # before
            content[term_pos:term_pos+len(search_terms[0])],
            content[term_pos+len(search_terms[0]):term_pos+len(search_terms[0])+100]
        )

        return {
            'title': detailed_data['title'],
            'url': detailed_data['url'],
            'cat': detailed_data['type'],
            'score': doc_weight,
            'preview': preview
        }


def generate_detailed_list(complete_list, search_query, start, length=20):
    search_terms = parse_text(search_query).split(' ')

    return [_generate_detailed_item(doc_id, doc_weight, search_terms) for
            doc_id, doc_weight in complete_list[start:start+length]]
