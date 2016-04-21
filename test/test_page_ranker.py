from nose import with_setup
import os
from tsg.config import DATA_DIR
from tsg.ranker.page_rank import parse_link, get_docs_for_target_doc
from tsg.crawler.downloader import get_site

RAW_TEST_DIRECTORY = DATA_DIR + "/test/files/raw/"
files = [RAW_TEST_DIRECTORY + "author_a_A:Almaaf_Bader_Ali.html", 
		 RAW_TEST_DIRECTORY + "author_m_Miao:Jian=Jun.html", 
		 RAW_TEST_DIRECTORY + "author_t_Tran:Quang=Dung.html", 
		 RAW_TEST_DIRECTORY + "journal_ijea_ijea5.html"]

def create_raw_directory():
	os.makedirs(RAW_TEST_DIRECTORY, exist_ok=True)

	#Check for some related files.
	urls = ["http://dblp.uni-trier.de/pers/hd/a/A:Almaaf_Bader_Ali",
			"http://dblp.uni-trier.de/pers/hd/m/Miao:Jian=Jun", 
	        "http://dblp.uni-trier.de/pers/hd/t/Tran:Quang=Dung",
	        "http://dblp.uni-trier.de/db/journals/ijea/ijea5.html"]

	for i, url in enumerate(urls):
		if os.path.exists(files[i]):
			pass
		else:
			webpage = get_site(url)
			with open(files[i], 'w') as f:
				f.write(webpage.text)

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

	test_link = "http://dblp.uni-trier.de/pers/hd/a/A:Almaaf_Bader_Ali"
	test_filename = "author_a_A:Almaaf_Bader_Ali.html"

	filename = parse_link(test_link)

	print(filename)

	assert filename[0] == test_filename

@with_setup(create_raw_directory, delete_raw_files)
def test_get_docs_for_target_doc():

	#define some docs in DATA_DIR/test/files to use here.
	test_doc_dict = {'author_h_Harris:Tom.html': ['journal_ijea_ijea5.html'], 
	'author_m_Muthaiyah:Saravanan.html': ['journal_ijea_ijea5.html'], 
	'author_a_A:Almaaf_Bader_Ali.html': ['journal_ijea_ijea5.html'], 
	'author_h_Huang:Dechun.html': ['journal_ijea_ijea5.html'], 
	'author_a_Abroud:Alireza.html': ['journal_ijea_ijea5.html'], 
	'author_s_Smith:Sheila.html': ['journal_ijea_ijea5.html'], 
	'author_h_Hsu:Huei=Hsia.html': ['journal_ijea_ijea5.html'], 
	'author_c_Chen:Bo=Ying.html': ['journal_ijea_ijea5.html'], 
	'author_l_Lin:Tzu=Hong.html': ['journal_ijea_ijea5.html'], 
	'author_h_Hanafizadeh:Mohammad_Reza.html': ['journal_ijea_ijea5.html'], 
	'author_h_Ho:Tai=Li.html': ['journal_ijea_ijea5.html'], 
	'author_h_Hanafizadeh:Payam.html': ['journal_ijea_ijea5.html'], 
	'author_t_Tran:Quangdung.html': ['journal_ijea_ijea5.html'], 
	'author_t_Tran:Quang=Dung.html': ['journal_ijea_ijea5.html'], 
	'author_a_Abdelghaffar:Hany.html': ['journal_ijea_ijea5.html'], 
	'author_z_Zhang:Jeff.html': ['journal_ijea_ijea5.html'], 
	'author_s_Smith:Sheila_M=.html': ['journal_ijea_ijea5.html'], 
	'author_m_Moustafa:Hussien.html': ['journal_ijea_ijea5.html'], 
	'author_h_Hsu:Pi=Fang.html': ['journal_ijea_ijea5.html'], 
	'author_d_Darisipudi:Ashok.html': ['journal_ijea_ijea5.html'], 
	'author_c_Coverdale:Tonjia_S=.html': ['journal_ijea_ijea5.html'], 
	'author_c_Choong:Yap_Voon.html': ['journal_ijea_ijea5.html'], 
	'author_z_Zhao:Jensen.html': ['journal_ijea_ijea5.html'], 
	'author_s_Shih:Tsui=Yii.html': ['journal_ijea_ijea5.html'], 
	'author_z_Zhou:Tao.html': ['journal_ijea_ijea5.html'], 
	'author_a_Alexander:Melody.html': ['journal_ijea_ijea5.html'], 
	'author_a_Alwahaishi:Saleh.html': ['journal_ijea_ijea5.html'], 
	'author_l_Lin:Shu=Yu.html': ['journal_ijea_ijea5.html'], 
	'author_m_Miao:Jian=Jun.html': ['journal_ijea_ijea5.html'], 
	'author_z_Zhang:Changzheng.html': ['journal_ijea_ijea5.html'], 
	'author_h_Hsing:San=San.html': ['journal_ijea_ijea5.html'], 
	'author_s_Sharma:Sushil_Kumar.html': ['journal_ijea_ijea5.html'], 
	'author_b_Bohlin:Erik.html': ['journal_ijea_ijea5.html'], 
	'author_t_Tsai:Chia=Wen.html': ['journal_ijea_ijea5.html'], 
	'author_c_Chen:Yi=Fen.html': ['journal_ijea_ijea5.html'], 
	'author_s_Saprikis:Vaggelis.html': ['journal_ijea_ijea5.html'], 
	'author_a_Al=Jenaibi:Badreya.html': ['journal_ijea_ijea5.html'], 
	'author_s_Sn=aacute=sel:V=aacute=clav.html': ['journal_ijea_ijea5.html'], 
	'author_l_Lu:Hsi=Peng.html': ['journal_ijea_ijea5.html'], 
	'author_w_Wilbon:Anthony_D=.html': ['journal_ijea_ijea5.html']}


	doc_dict = get_docs_for_target_doc(RAW_TEST_DIRECTORY)

	assert doc_dict == test_doc_dict