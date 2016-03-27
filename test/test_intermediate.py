from nose.tools import eq_
from unittest import TestCase
import os
import shutil

from tsg.intermediate.base import process_document
from tsg.intermediate import generate_intermediate
from tsg.config import INTERMEDIATE_DIR, PARSED_DIR

# if file not exist, add header first
# every document adds one line to all existing terms
# simple test for counting words
#


def test_generate_intermediate():
    '''reads a json file and counts the words occurences'''
    target_aa_csv = 'test/files/aa.csv'
    target_journal_csv = 'test/files/journal.csv'

    file_uuid1 = '598859a0-eaa7-466a-8919-e6260c89edef'
    file_uuid2 = '31a8e3b4-8c67-4fb7-b11a-1df1105617a2'

    os.makedirs(PARSED_DIR, exist_ok=True)
    for file_uuid in [file_uuid1, file_uuid2]:
        shutil.copy('test/files/{}.json'.format(file_uuid), PARSED_DIR)

    generate_intermediate(file_uuid1)
    generate_intermediate(file_uuid2)

    # check that output files match
    with open(target_aa_csv) as target_file:
        with open(INTERMEDIATE_DIR+'aa.csv') as output_file:
            eq_(target_file.read(), output_file.read())

    with open(target_journal_csv) as target_file:
        with open(INTERMEDIATE_DIR+'journal.csv') as output_file:
            eq_(target_file.read(), output_file.read())


class TestProcessDocument(TestCase):
    def test_process_document(self):
        file_uuid = '598859a0-eaa7-466a-8919-e6260c89edef'
        # mv test file to  '{}{}.json'.format(PARSED_DIR, file_uuid)
        os.makedirs(PARSED_DIR, exist_ok=True)
        shutil.copy('test/files/{}.json'.format(file_uuid), PARSED_DIR)

        wordlist = process_document('{}{}.json'.format(PARSED_DIR, file_uuid))

        self.assertCountEqual(
            wordlist,
            [('aa', {'title': 1, 'isbn': 0, 'content': 3, 'type': 0}),
             ('journal', {'title': 0, 'isbn': 0, 'content': 1, 'type': 1})])
