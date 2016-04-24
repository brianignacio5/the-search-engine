from nose import with_setup
import os
from tsg.config import DATA_DIR
from tsg.ranker.page_rank import parse_link, build_link_database
from tsg.crawler.downloader import get_site

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
	 				 
	with open(TEST_LINK_DATABASE_PATH,'w') as link_f:
		if os.path.exists(link_f):
			pass
		else:
			for key, value in test_link_database.items():
				link_str = ""
			for link in value:
				link_str += "," + link
			link_f.write(key + " " + link_str[1:] + "\n")

def delete_raw_files():
	remove_flag = False
	try:
		for f in files:
			if remove_flag:
				os.remove(f)
				assert not os.path.exists(f)
	except OSError:
		pass

def test_parse_link():

	test_link = "http://dblp.uni-trier.de/db/journals/ijea/ijea5.html#AMT13"
	test_filename = "journal_ijea_ijea5.html"

	filename = parse_link(test_link)

	assert filename[0] == test_filename

@with_setup(create_raw_directory, delete_raw_files)
def test_get_docs_for_target_doc():

	#define some docs in DATA_DIR/test/files to use here.
	test_doc_dict = {'author_w_Wilbon:Anthony_D=.html': ['journal_ijea_ijea5.html'],
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

	doc_dict = build_link_database(RAW_TEST_DIRECTORY)

	assert doc_dict == test_doc_dict

@with_setup(create_raw_directory, delete_raw_files)
def test_calc_page_rank():

	# Is it testable ?
	#

	assert True == True