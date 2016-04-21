from nose import with_setup
import os
from tsg.config import DATA_DIR
from tsg.ranker.page_rank import parse_link, get_docs_for_target_doc
from tsg.crawler.downloader import get_site

RAW_TEST_DIRECTORY = DATA_DIR + "/test/files/"
files = [RAW_TEST_DIRECTORY + "filename.html", 
		 RAW_TEST_DIRECTORY + "filename.html", 
		 RAW_TEST_DIRECTORY + "filename.html"]

def create_raw_directory():
	os.makedirs(RAW_TEST_DIRECTORY, exist_ok=True)

	#Check for some related files.
	urls = ["file_1_url", "file_2_url", "file_3_url"]

	for i, url in enumerate(urls):
		webpage = get_site(url)
		with open(files[i], 'w') as f:
			f.write(webpage.text)

def delete_raw_files():
	try:
		for f in files:
			os.remove(f)
	except OSError:
		pass

	for f in files:
		assert not os.path.exists(f)
	
def test_parse_link():

	test_link = ""
	test_filename = ""

	filename = parse_link(test_link)

	assert filename == test_filename

@with_setup(create_raw_directory, delete_raw_files)
def test_get_docs_for_target_doc():

	#define some docs in DATA_DIR/test/files to use here.
	test_doc_dict = {"filename": 0}

	doc_dict = get_docs_for_target_doc(RAW_TEST_DIRECTORY)

	assert doc_dict == test_doc_dict