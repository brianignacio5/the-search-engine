from nose import with_setup
import os
from lxml import etree
from tsg.config import DATA_DIR
from tsg.ranker.page_rank import parse_link, build_link_database, get_page_outlinks, get_doc_inlinks, calc_page_rank
from tsg.crawler.downloader import get_site
from tsg.crawler.base import crawl_site

RAW_TEST_DIRECTORY = DATA_DIR + "/test/files/raw/"
files = [RAW_TEST_DIRECTORY + "author_a_A:Almaaf_Bader_Ali.html",
		 RAW_TEST_DIRECTORY + "journal_ijea_ijea5.html",
		 RAW_TEST_DIRECTORY + "conference_aaip_aaip2009.html"]

TEST_LINK_DATABASE_PATH = DATA_DIR + "test_link_database.dat"

def create_raw_directory():
	os.makedirs(RAW_TEST_DIRECTORY, exist_ok=True)

	#Check for some related files.
	urls = ["http://dblp.uni-trier.de/pers/hd/a/A:Almaaf_Bader_Ali",
	        "http://dblp.uni-trier.de/db/journals/ijea/ijea5.html",
	        "http://dblp.uni-trier.de/db/conf/aaip/aaip2009.html"]

	for i, url in enumerate(urls):
		if os.path.exists(files[i]):
			pass
		else:
			webpage = get_site(url)
			with open(files[i], 'w') as f:
				f.write(webpage.text)

	test_link_database = {'author_w_Wilbon:Anthony_D=.html': ['journal_ijea_ijea5.html'],
	 				 'author_h_Harris:Tom.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Smith:Sheila_M=.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Sharma:Sushil_Kumar.html': ['journal_ijea_ijea5.html'], 
	 				 'author_r_Ram=iacute=rez=Quintana:M=_Jos=eacute=.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_c_Chen:Yi=Fen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Henderson:Robert.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hern=aacute=ndez=Orallo:Jos=eacute=.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_z_Zhang:Changzheng.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Saprikis:Vaggelis.html': ['journal_ijea_ijea5.html'], 
	 				 'author_e_Estruch:Vicent.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Alwahaishi:Saleh.html': ['journal_ijea_ijea5.html'], 
	 				 'author_k_Koopman:Pieter_W=_M=.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hieber:Thomas.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Al=Jenaibi:Badreya.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhou:Tao.html': ['journal_ijea_ijea5.html'], 
	 				 'author_c_Chen:Bo=Ying.html': ['journal_ijea_ijea5.html'], 
	 				 'author_b_Bohlin:Erik.html': ['journal_ijea_ijea5.html'], 
	 				 'author_t_Tran:Quangdung.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Huang:Dechun.html': ['journal_ijea_ijea5.html'], 
	 				 'author_t_Tsai:Chia=Wen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Miao:Jian=Jun.html': ['journal_ijea_ijea5.html', 'author_a_A:Almaaf_Bader_Ali.html', 'author_t_Tran:Quang=Dung.html'], 
	 				 'author_k_Kitzelmann:Emanuel.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hsing:San=San.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Smith:Sheila.html': ['journal_ijea_ijea5.html'], 
	 				 'author_d_Darisipudi:Ashok.html': ['journal_ijea_ijea5.html'],
	 				 'author_a_A:Almaaf_Bader_Ali.html': ['journal_ijea_ijea5.html', 'author_t_Tran:Quang=Dung.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'journal_journals_lncs.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Alexander:Melody.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hofmann_0008:Martin.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_t_Tran:Quang=Dung.html': ['journal_ijea_ijea5.html', 'author_a_A:Almaaf_Bader_Ali.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'author_a_Abdelghaffar:Hany.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Muthaiyah:Saravanan.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhao:Jensen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Sn=aacute=sel:V=aacute=clav.html': ['journal_ijea_ijea5.html'], 
	 				 'author_y_Yakushev:Alexey_Rodriguez.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_c_Coverdale:Tonjia_S=.html': ['journal_ijea_ijea5.html'], 
	 				 'journal_ijea_ijea5.html': ['author_a_A:Almaaf_Bader_Ali.html', 'author_t_Tran:Quang=Dung.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'author_h_Hsu:Huei=Hsia.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hanafizadeh:Mohammad_Reza.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lu:Hsi=Peng.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Mitchell:Neil.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_m_Moustafa:Hussien.html': ['journal_ijea_ijea5.html'], 
	 				 'author_c_Choong:Yap_Voon.html': ['journal_ijea_ijea5.html'], 
	 				 'author_f_Ferri:C=eacute=sar.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_k_Katayama:Susumu.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Ho:Tai=Li.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hanafizadeh:Payam.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lin:Tzu=Hong.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lin:Shu=Yu.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhang:Jeff.html': ['journal_ijea_ijea5.html'], 
	 				 'author_j_Jeuring:Johan.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_s_Schmid:Ute.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_s_Shih:Tsui=Yii.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hsu:Pi=Fang.html': ['journal_ijea_ijea5.html'], 
	 				 'author_a_Abroud:Alireza.html': ['journal_ijea_ijea5.html'], 
	 				 'author_p_Plasmeijer:Rinus.html': ['conference_aaip_aaip2009.html']}
	 				 
	if not os.path.exists(TEST_LINK_DATABASE_PATH):
		with open(TEST_LINK_DATABASE_PATH,'w') as link_f:
			for key, value in test_link_database.items():
				link_str = ""
				for link in value:
					link_str += "," + link
				link_f.write(key + " " + link_str[1:] + "\n")

	# for f in files:
	# 	download_outlinks_by_filename(f)

def download_outlinks_by_filename(file_path):
	xpath_string = "//div[@class='data']//a/@href"
	parser = etree.HTMLParser()
	outlinks = []
	
	with open(file_path) as doc_f:
		tree = etree.parse(doc_f, parser)
		outlinks = tree.xpath(xpath_string)

	for link in outlinks:
		document_type = parse_link(link)[1]
		crawl_site(link, document_type)


def delete_raw_files():
	remove_flag = False
	try:
		if remove_flag:
			for f in files:
				os.remove(f)
				assert not os.path.exists(f)
			os.remove(TEST_LINK_DATABASE_PATH)
			assert not os.path.exists(TEST_LINK_DATABASE_PATH)
	except OSError:
		pass

def test_parse_link():

	test_link = "http://dblp.uni-trier.de/db/journals/ijea/ijea5.html#AMT13"
	test_filename = "journal_ijea_ijea5.html"

	filename = parse_link(test_link)

	assert filename[0] == test_filename

def test_get_page_outlinks():
	test_filename = RAW_TEST_DIRECTORY + "author_a_A:Almaaf_Bader_Ali.html"

	test_outlinks = ['author_m_Miao:Jian=Jun.html', 
					 'author_t_Tran:Quang=Dung.html',
					 'journal_ijea_ijea5.html']

	outlinks_by_function = get_page_outlinks(test_filename)

	assert outlinks_by_function == test_outlinks

@with_setup(create_raw_directory, delete_raw_files)
def test_build_link_database():

	#define some docs in DATA_DIR/test/files to use here.
	test_doc_dict = {'author_w_Wilbon:Anthony_D=.html': ['journal_ijea_ijea5.html'],
	 				 'author_h_Harris:Tom.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Smith:Sheila_M=.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Sharma:Sushil_Kumar.html': ['journal_ijea_ijea5.html'], 
	 				 'author_r_Ram=iacute=rez=Quintana:M=_Jos=eacute=.html': 
	 				 	['conference_aaip_aaip2009.html'], 
	 				 'author_c_Chen:Yi=Fen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Henderson:Robert.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hern=aacute=ndez=Orallo:Jos=eacute=.html': 
	 				 	['conference_aaip_aaip2009.html'], 
	 				 'author_z_Zhang:Changzheng.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Saprikis:Vaggelis.html': ['journal_ijea_ijea5.html'], 
	 				 'author_e_Estruch:Vicent.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Alwahaishi:Saleh.html': ['journal_ijea_ijea5.html'], 
	 				 'author_k_Koopman:Pieter_W=_M=.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hieber:Thomas.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Al=Jenaibi:Badreya.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhou:Tao.html': ['journal_ijea_ijea5.html'], 
	 				 'author_c_Chen:Bo=Ying.html': ['journal_ijea_ijea5.html'], 
	 				 'author_b_Bohlin:Erik.html': ['journal_ijea_ijea5.html'], 
	 				 'author_t_Tran:Quangdung.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Huang:Dechun.html': ['journal_ijea_ijea5.html'], 
	 				 'author_t_Tsai:Chia=Wen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Miao:Jian=Jun.html': ['journal_ijea_ijea5.html', 
	 				 	'author_a_A:Almaaf_Bader_Ali.html', 'author_t_Tran:Quang=Dung.html'], 
	 				 'author_k_Kitzelmann:Emanuel.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Hsing:San=San.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Smith:Sheila.html': ['journal_ijea_ijea5.html'], 
	 				 'author_d_Darisipudi:Ashok.html': ['journal_ijea_ijea5.html'],
	 				 'author_a_A:Almaaf_Bader_Ali.html': ['journal_ijea_ijea5.html', 
	 				 	'author_t_Tran:Quang=Dung.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'journal_journals_lncs.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_a_Alexander:Melody.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hofmann_0008:Martin.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_t_Tran:Quang=Dung.html': ['journal_ijea_ijea5.html', 
	 				 	'author_a_A:Almaaf_Bader_Ali.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'author_a_Abdelghaffar:Hany.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Muthaiyah:Saravanan.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhao:Jensen.html': ['journal_ijea_ijea5.html'], 
	 				 'author_s_Sn=aacute=sel:V=aacute=clav.html': ['journal_ijea_ijea5.html'], 
	 				 'author_y_Yakushev:Alexey_Rodriguez.html': 
	 				 	['conference_aaip_aaip2009.html'], 
	 				 'author_c_Coverdale:Tonjia_S=.html': ['journal_ijea_ijea5.html'], 
	 				 'journal_ijea_ijea5.html': ['author_a_A:Almaaf_Bader_Ali.html', 
	 				 	'author_t_Tran:Quang=Dung.html', 'author_m_Miao:Jian=Jun.html'], 
	 				 'author_h_Hsu:Huei=Hsia.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hanafizadeh:Mohammad_Reza.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lu:Hsi=Peng.html': ['journal_ijea_ijea5.html'], 
	 				 'author_m_Mitchell:Neil.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_m_Moustafa:Hussien.html': ['journal_ijea_ijea5.html'], 
	 				 'author_c_Choong:Yap_Voon.html': ['journal_ijea_ijea5.html'], 
	 				 'author_f_Ferri:C=eacute=sar.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_k_Katayama:Susumu.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_h_Ho:Tai=Li.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hanafizadeh:Payam.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lin:Tzu=Hong.html': ['journal_ijea_ijea5.html'], 
	 				 'author_l_Lin:Shu=Yu.html': ['journal_ijea_ijea5.html'], 
	 				 'author_z_Zhang:Jeff.html': ['journal_ijea_ijea5.html'], 
	 				 'author_j_Jeuring:Johan.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_s_Schmid:Ute.html': ['conference_aaip_aaip2009.html'], 
	 				 'author_s_Shih:Tsui=Yii.html': ['journal_ijea_ijea5.html'], 
	 				 'author_h_Hsu:Pi=Fang.html': ['journal_ijea_ijea5.html'], 
	 				 'author_a_Abroud:Alireza.html': ['journal_ijea_ijea5.html'], 
	 				 'author_p_Plasmeijer:Rinus.html': ['conference_aaip_aaip2009.html']}

	doc_dict = build_link_database(RAW_TEST_DIRECTORY)

	assert doc_dict == test_doc_dict

@with_setup(create_raw_directory, delete_raw_files)
def test_get_doc_inlinks():

	filename = "author_a_A:Almaaf_Bader_Ali.html"

	test_inlinks = ['journal_ijea_ijea5.html', 
					'author_t_Tran:Quang=Dung.html', 
					'author_m_Miao:Jian=Jun.html']
	
	doc_inlinks_by_function = get_doc_inlinks(filename, TEST_LINK_DATABASE_PATH)

	assert doc_inlinks_by_function == test_inlinks

@with_setup(create_raw_directory, delete_raw_files)
def test_calc_page_rank():

	test_pagerank_per_doc = [('journal_ijea_ijea5.html', 1), 
							 ('author_t_Tran:Quang=Dung.html', 0.7373983739837399), 
							 ('author_m_Miao:Jian=Jun.html', 0.7373983739837399), 
							 ('author_a_A:Almaaf_Bader_Ali.html', 0.7373983739837399), 
							 ('author_z_Zhou:Tao.html', 0.17073170731707318), 
							 ('author_z_Zhang:Jeff.html', 0.17073170731707318), 
							 ('author_w_Wilbon:Anthony_D=.html', 0.17073170731707318), 
							 ('author_t_Tsai:Chia=Wen.html', 0.17073170731707318), 
							 ('author_t_Tran:Quangdung.html', 0.17073170731707318), 
							 ('author_s_Sn=aacute=sel:V=aacute=clav.html', 0.17073170731707318), 
							 ('author_s_Smith:Sheila_M=.html', 0.17073170731707318), 
							 ('author_s_Smith:Sheila.html', 0.17073170731707318), 
							 ('author_s_Shih:Tsui=Yii.html', 0.17073170731707318), 
							 ('author_s_Sharma:Sushil_Kumar.html', 0.17073170731707318), 
							 ('author_s_Saprikis:Vaggelis.html', 0.17073170731707318), 
							 ('author_m_Muthaiyah:Saravanan.html', 0.17073170731707318), 
							 ('author_m_Moustafa:Hussien.html', 0.17073170731707318), 
							 ('author_l_Lu:Hsi=Peng.html', 0.17073170731707318), 
							 ('author_l_Lin:Tzu=Hong.html', 0.17073170731707318), 
							 ('author_l_Lin:Shu=Yu.html', 0.17073170731707318), 
							 ('author_h_Huang:Dechun.html', 0.17073170731707318), 
							 ('author_h_Hsu:Huei=Hsia.html', 0.17073170731707318), 
							 ('author_h_Hsing:San=San.html', 0.17073170731707318), 
							 ('author_h_Ho:Tai=Li.html', 0.17073170731707318), 
							 ('author_h_Hanafizadeh:Payam.html', 0.17073170731707318), 
							 ('author_h_Hanafizadeh:Mohammad_Reza.html', 0.17073170731707318), 
							 ('author_d_Darisipudi:Ashok.html', 0.17073170731707318), 
							 ('author_c_Coverdale:Tonjia_S=.html', 0.17073170731707318), 
							 ('author_c_Choong:Yap_Voon.html', 0.17073170731707318), 
							 ('author_c_Chen:Yi=Fen.html', 0.17073170731707318), 
							 ('author_c_Chen:Bo=Ying.html', 0.17073170731707318), 
							 ('author_b_Bohlin:Erik.html', 0.17073170731707318), 
							 ('author_a_Alwahaishi:Saleh.html', 0.17073170731707318), 
							 ('author_a_Alexander:Melody.html', 0.17073170731707318), 
							 ('author_a_Al=Jenaibi:Badreya.html', 0.17073170731707318), 
							 ('author_a_Abroud:Alireza.html', 0.17073170731707318), 
							 ('author_a_Abdelghaffar:Hany.html', 0.17073170731707318), 
							 ('journal_journals_lncs.html', 0.15000000000000002), 
							 ('author_y_Yakushev:Alexey_Rodriguez.html', 0.15000000000000002), 
							 ('author_s_Schmid:Ute.html', 0.15000000000000002), 
							 ('author_r_Ram=iacute=rez=Quintana:M=_Jos=eacute=.html', 0.15000000000000002), 
							 ('author_p_Plasmeijer:Rinus.html', 0.15000000000000002), 
							 ('author_m_Mitchell:Neil.html', 0.15000000000000002), 
							 ('author_k_Koopman:Pieter_W=_M=.html', 0.15000000000000002), 
							 ('author_k_Katayama:Susumu.html', 0.15000000000000002), 
							 ('author_j_Jeuring:Johan.html', 0.15000000000000002), 
							 ('author_h_Hern=aacute=ndez=Orallo:Jos=eacute=.html', 0.15000000000000002), 
							 ('author_h_Henderson:Robert.html', 0.15000000000000002), 
							 ('author_f_Ferri:C=eacute=sar.html', 0.15000000000000002)]

	pagerank_per_doc = calc_page_rank(TEST_LINK_DATABASE_PATH)

	assert pagerank_per_doc == test_pagerank_per_doc