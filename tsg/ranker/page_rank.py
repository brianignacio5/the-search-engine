import re
from lxml import etree
import glob, os
from tsg.config import RAW_DIR

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

def build_link_database(html_files_path= RAW_DIR):
	doc_dict = {}
	# xpath_string = "//div[@id='main']/ul[@class='publ-list']//span/a/@href"
	xpath_string = "//div[@class='data']//a/@href" # OK for Journals and authors
	parser = etree.HTMLParser()
	os.chdir(html_files_path)
	for doc_filename in glob.glob("*.html"):
		doc_path = html_files_path + doc_filename
		with open(doc_path, 'r') as doc:
			tree = etree.parse(doc, parser)
			target_doc_links = tree.xpath(xpath_string) #Get links doc_path
			# Classify links to author, journal and conference.
			for target_doc_link in target_doc_links:
				[target_doc, doc_type] = parse_link(target_doc_link)
				#Return doc_filename and doc_type: author, conference or journal
				if doc_type in ["author", "conference", "journal"]:
					if (target_doc in doc_dict and doc_filename not in doc_dict[target_doc]):
						# doc_dict[target_doc] = [doc_dict[target_doc], doc_filename]
						doc_dict[target_doc].append(doc_filename)
					elif target_doc not in doc_dict:
						doc_dict[target_doc] = [doc_filename]

	return doc_dict

def calc_page_rank(doc_filename, link_database_path):

	# Something nice
	doc_inlinks= []

	with open(link_database_path) as link_db:
		for line in link_db:
			if line.startswith(doc_filename):
				doc_inlinks = list(line[len(doc_filename)+1:].split(','))

	return 0