import os
import tsg.indexer.page_rank as page_rank

RAW_TEST_DIRECTORY = os.path.abspath('test') + "/files/pagerank/"
files = [RAW_TEST_DIRECTORY + "author_a_A:Almaaf_Bader_Ali.html",
		 RAW_TEST_DIRECTORY + "journal_ijea_ijea5.html",
		 RAW_TEST_DIRECTORY + "conference_aaip_aaip2009.html"]

def test_parse_link():

	test_link = "http://dblp.uni-trier.de/db/journals/ijea/ijea5.html#AMT13"
	test_filename = "journal_ijea_ijea5.html"

	filename = page_rank.parse_link(test_link)

	assert filename[0] == test_filename

def test_get_page_outlinks():
	test_filename = RAW_TEST_DIRECTORY + "author_a_A:Almaaf_Bader_Ali.html"
	test_outlinks = ['author_m_Miao:Jian=Jun.html',
					 'author_t_Tran:Quang=Dung.html',
					 'journal_ijea_ijea5.html']

	outlinks_by_function = page_rank.get_page_outlinks(test_filename)

	assert outlinks_by_function == test_outlinks

def test_build_link_database():

	#define some docs in DATA_DIR/test/files to use here.
	test_doc_dict = {'journal_ijea_ijea5.html': ['author_a_A:Almaaf_Bader_Ali.html'],
					 'journal_journals_lncs.html': ['conference_aaip_aaip2009.html'],
					 'author_y_Yakushev:Alexey_Rodriguez.html': ['conference_aaip_aaip2009.html']}

	doc_dict = page_rank.build_link_database(RAW_TEST_DIRECTORY)
	
	for doc in test_doc_dict:
		assert doc in doc_dict

def test_calc_page_rank():

	test_pagerank_per_doc = [('author_t_Tran:Quang=Dung.html', 0.19765190942368532),
							 ('author_a_Al=Jenaibi:Badreya.html', 0.15401443776897214),
							 ('author_h_Henderson:Robert.html', 0)]

	pagerank_per_doc = page_rank.calc_page_rank(RAW_TEST_DIRECTORY)

	for key, value in test_pagerank_per_doc:
		assert key in pagerank_per_doc
