import re
from collections import deque, OrderedDict
from lxml import etree
import glob, os
from tsg.config import RAW_DIR, DATA_DIR
import operator

def parse_link(doc_link):
	'''
	Define a function which take a link and obtain the doc_filename string
	and the type of document: journal, conference or author.
	'''
	link_parts = list(re.search('([^/]*)/([^/]*)$', doc_link).groups())

	if "#" in link_parts[1]:
		link_parts[1] = link_parts[1].split("#")[0]

	if "pers" in doc_link :
		category = "author"
	elif "conf" in doc_link:
		category = "conference"
	elif "journals" in doc_link:
		category = "journal"
	else:
		category = ""

	doc_filename = '{}_{}_{}{}'.format(category,
                                   link_parts[0],
                                   link_parts[1],
                                   '' if link_parts[1][-5:] == '.html'
                                   else'.html')

	return [doc_filename, category]

def get_page_outlinks(doc_path):
	xpath_string = "//div[@class='data']//a/@href"
	parser = etree.HTMLParser()
	page_outlinks = []
	page_outfiles = []

	with open(doc_path) as doc_f:
		tree = etree.parse(doc_f, parser)
		page_outlinks = tree.xpath(xpath_string)

	for link in page_outlinks:
		page_outfiles.append(parse_link(link)[0])

	return page_outfiles

def build_link_database(html_files_path= RAW_DIR):
	doc_dict = {}
	# xpath_string = "//div[@id='main']/ul[@class='publ-list']//span/a/@href"
	os.chdir(html_files_path)
	for doc_filename in glob.glob("*.html"):
		doc_path = html_files_path + doc_filename
		doc_outlinks = get_page_outlinks(doc_path)
		for target_doc in doc_outlinks:
				#[target_doc, doc_type] = parse_link(target_doc_link)
				doc_type = target_doc.split('_')[0]
				#Return doc_filename and doc_type: author, conference or journal
				if doc_type in ["author", "conference", "journal"]:
					if (target_doc in doc_dict and doc_filename not in doc_dict[target_doc]):
						# doc_dict[target_doc] = [doc_dict[target_doc], doc_filename]
						doc_dict[target_doc].append(doc_filename)
					elif target_doc not in doc_dict:
						doc_dict[target_doc] = [doc_filename]
	# Sort alphabetically
	ordered_db = OrderedDict(sorted(doc_dict.items(), key= lambda t: t[0])) 

	LINK_DATABASE_PATH = DATA_DIR + "link_database.dat" #Replace LINK_DATABASE_PATH in config

	if not os.path.exists(DATA_DIR): 
		with open(LINK_DATABASE_PATH,'w') as link_f:
			for key, value in ordered_db.items():
				link_str = ""
				for link in value:
					link_str += "," + link
				link_f.write(key + " " + link_str[1:] + "\n")

	return ordered_db

def get_doc_inlinks(doc_filename, link_database_path):
	doc_inlinks = []
	with open(link_database_path) as link_db:
		for line in link_db:
			if line.startswith(doc_filename):
				doc_inlinks = list(line[len(doc_filename)+1:].strip().split(','))

	return doc_inlinks

def calc_page_rank(link_database_path):

	# Something nice
	d = 0.85 # Damping in PageRank Algorithm
	threshold = 0.0000001 # 1x 10^-6
	iteration_flag = True # Keep page rank iteration until threshold is met

	link_db_docs_queue = deque()
	doc_inlinks = {}
	doc_outlinks = {}
	pagerank_per_doc = {}

	with open(link_database_path) as link_db:
		for line in link_db:
			current_doc = line.split(' ')[0]
			doc_inlinks[current_doc] = list(line[len(current_doc)+1:].strip().split(','))
			doc_outlinks[current_doc] = get_page_outlinks(RAW_DIR + current_doc)
			link_db_docs_queue.append(current_doc)
			pagerank_per_doc[current_doc] = 1

	while iteration_flag:
		tmp_queue = link_db_docs_queue
		tmp_pagerank_per_doc = {}

		while len(tmp_queue) > 0:
			#page rank pop of queue
			current_doc_in_queue = tmp_queue.pop()
			tmp_pagerank_per_doc[current_doc_in_queue] = (1 - d)
			for inlink in doc_inlinks[current_doc_in_queue]:
				num_outlinks_per_inlink = 0
				if inlink in doc_outlinks.keys():
					num_outlinks_per_inlink = len(doc_outlinks[inlink])
					tmp_pagerank_per_doc[current_doc_in_queue] += d*(pagerank_per_doc[inlink] 
						/ num_outlinks_per_inlink)
				else:
					pass

		for doc in tmp_pagerank_per_doc:
			if (pagerank_per_doc[doc] - tmp_pagerank_per_doc[doc] < threshold):
				iteration_flag = False
			else:
				pagerank_per_doc[doc] = tmp_pagerank_per_doc[doc]

	sorted_pagerank_per_docs = sorted(pagerank_per_doc.items(), 
		key = operator.itemgetter(1,0), reverse = True)

	return sorted_pagerank_per_docs