import re
from lxml import html
import glob, os
from tsg.config import RAW_DIR

def parse_link(doc_link):
	'''
	Define a function which take a link and obtain the doc_filename string
	and the type of document: journal, conference or author.
	'''
	link_parts = re.search('([^/]*)/([^/]*)$', doc_link).groups()

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

def get_docs_for_target_doc(html_files_path= RAW_DIR):
	doc_dict = {}
	os.chdir(html_files_path)
	for doc_path in glob.glob("*.html"):
		with open(doc_path) as doc:
			tree = html.fromstring(doc)
			target_doc_links = tree.xpath("//div[@id='main']/span/a/@href") #Get links doc_path

			# Classify links to author, journal and conference.
			for target_doc_link in target_doc_links:
				[target_doc, doc_type] = parse_link(target_doc_link)
				#Return doc_filename and doc_type: author, conference or journal
				if doc_type in ["author", "conference", "journal"]:
					doc_dict[target_doc].append(doc)
	return doc_dict
