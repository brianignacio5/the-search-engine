import re
from collections import OrderedDict
from lxml import etree
import glob, os
from tsg.config import RAW_DIR, INDEXINFO_PATH
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

	if os.path.exists(doc_path):
		with open(doc_path) as doc_f:
			tree = etree.parse(doc_f, parser)
			page_outlinks = tree.xpath(xpath_string)

	for link in page_outlinks:
		page_outfiles.append(parse_link(link)[0])

	return page_outfiles

def build_link_database(html_files_path= RAW_DIR):
	doc_dict = {}
	for doc_filename in os.listdir(html_files_path):
		if doc_filename.endswith(".html"):
			doc_path = html_files_path + doc_filename
			doc_outlinks = get_page_outlinks(doc_path)
			for target_doc in doc_outlinks:
				doc_type = target_doc.split('_')[0]
				if doc_type in ["author", "conference", "journal"]:
					if (target_doc in doc_dict and doc_filename not in doc_dict[target_doc]):
						doc_dict[target_doc].append(doc_filename)
					elif target_doc not in doc_dict:
						doc_dict[target_doc] = [doc_filename]
	# Sort alphabetically
	ordered_db = OrderedDict(sorted(doc_dict.items(), key= lambda t: t[0])) 

	return ordered_db

def calc_page_rank(html_files_path=RAW_DIR):

	d = 0.85 # Damping in PageRank Algorithm
	threshold = 0.0000001 # 1x 10^-6
	iteration_flag = True # Keep page rank iteration until threshold is met
	doc_inlinks = {}
	doc_outlinks = {}
	pagerank_per_doc = {}

	docs__links_db = build_link_database(html_files_path)

	for doc in docs__links_db.keys():
		doc_inlinks[doc] = docs__links_db[doc]
		doc_outlinks[doc] = get_page_outlinks(html_files_path + doc)
		pagerank_per_doc[doc] = 1

	while iteration_flag:
		tmp_pagerank_per_doc = {}
		for doc, doc_inlinks in docs__links_db.items():
			tmp_pagerank_per_doc[doc] = (1 - d)
			for inlink in doc_inlinks:
				num_outlinks_per_inlink = 0
				if inlink in doc_outlinks.keys():
					num_outlinks_per_inlink = len(doc_outlinks[inlink])
					tmp_pagerank_per_doc[doc] += d*(pagerank_per_doc[inlink] 
						/ num_outlinks_per_inlink)
				else:
					tmp_pagerank_per_doc[doc] = 0

		for doc in tmp_pagerank_per_doc:
			if (pagerank_per_doc[doc] - tmp_pagerank_per_doc[doc] < threshold):
				iteration_flag = False
			else:
				pagerank_per_doc[doc] = tmp_pagerank_per_doc[doc]
				iteration_flag = True

	sorted_pagerank_per_docs = OrderedDict(sorted(pagerank_per_doc.items(), 
		key = operator.itemgetter(1,0), reverse = True))

	return sorted_pagerank_per_docs