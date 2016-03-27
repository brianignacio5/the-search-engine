#!/usr/bin/env python
import nose
from nose.tools import eq_
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
    input_file = 'test/files/ftml_ftml2.html'
    with open('test/files/ftml_ftml2_words.json') as f:
        extracted_words_target = json.load(f)
    title, words = extract_content(input_file)
    eq_(extracted_words_target['words'], words)
    eq_(title, 'Foundations and Trends in Machine Learning, Volume 2')


def test_parse_document():
    input_file = 'test/files/ftml_ftml2.html'
    output_file = 'test/files/ftml_ftml2.json'
    target_output_file = 'test/files/ftml_ftml2_target.json'
    #  url = 'http://dblp.uni-trier.de/db/journals/ftml/ftml2.html'

    with open(target_output_file) as f:
        target_dict = json.load(f)

    parse_document('journal', input_file, output_file)
    with open(output_file) as f:
        output_dict = json.load(f)

    assert output_dict['uuid'] != ''
    target_dict['uuid'] = output_dict['uuid']

    eq_(target_dict, output_dict)

if __name__ == "__main__":
    nose.run()
