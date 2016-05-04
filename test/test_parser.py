#!/usr/bin/env python
import nose
from nose.tools import eq_
import os

from tsg import config
import json
from tsg.parser import parse_document
from tsg.parser.base import extract_content, parse_text



def test_text_conversion():
    unparseds = ['+{/}', 'hall+iae', 'holae+', 'Hello', 'hello', 'Jon-Doe',
                 'this is what we want. ThiSSI-lael3']
    parseds = ['', 'halliae', 'holae', 'hello', 'hello', 'jon doe',
               'this is what we want thissi lael3']

    for unparsed, parsed in zip(unparseds, parseds):
        eq_(parse_text(unparsed), parsed)


def test_extract_words():
    input_file = 'test/files/journal_ftml_ftml2.html'
    with open('test/files/journal_ftml_ftml2_words.json') as f:
        extracted_words_target = json.load(f)
    title, words, isbn, listings_count = extract_content(input_file)
    eq_(isbn, '')
    eq_(extracted_words_target['words'], words)
    eq_(title,
        'Foundations and Trends in Machine Learning, Volume 2 slash/word')
    eq_(listings_count, 4)


def test_parse_document():
    input_file = 'test/files/journal_ftml_ftml2.html'
    target_output_file = 'test/files/journal_ftml_ftml2_target.json'

    uuid = os.path.splitext(os.path.basename(input_file))[0]

    output_file = '{}{}.json'.format(config.PARSED_DIR, uuid)
    #  url = 'http://dblp.uni-trier.de/db/journals/ftml/ftml2.html'
    #


    with open(target_output_file) as f:
        target_dict = json.load(f)

    parse_document('journal', input_file)
    with open(output_file) as f:
        output_dict = json.load(f)

    target_dict['uuid'] = uuid

    eq_(target_dict, output_dict)

if __name__ == "__main__":
    nose.run()
