## Base Code 
from lxml import html
import requests
import re
import os
from tsg.config import RAW_DIR
## crawl_site, crawl_urls

def crawl_site(url):
   webpage = requests.get(url);
   filename = re.search('([^/]*)/([^/]*)$', url).group(0).replace('/','_') + '.html';
   doc_path = RAW_DIR + filename;
   with open(doc_path,'w') as f:
      f.write(webpage.text)
		
def crawl_urls(url):
   webpage = requests.get(url)
   tree = html.fromstring(webpage.content)
   authors = tree.xpath('//div[@id="browse-person-output"]/div[@class="columns hide-body"]/div/ul/li/a/@href')
   authors_urls = []
   for author_url in authors:
      authors_urls.append(author_url)
   return authors_urls
   n = 1
   while true:
   		300authors=crawl_urls('http://dblp.uni-trier.de/pers?pos=' + n)
   		for author_url in 300authors:
   			crawl_site(author_url)
   		n+=300


def crawl_url_journal(url):
	webpage = requests.get (url)
	tree = html.fromstring(webpage.content)
	journal = tree.xpath('//div[@id="browse-journal-output"]/div[@class="hide-body"]/ul/li/a/@href')
	journal_url =[]
	for journal_url in journal:
		journal_url.append(journal_url)
	return journal_url
	n = 1
    while true:
   		200journal=crawl_url_journal('http://dblp.uni-trier.de/db/journals/?pos=' + n)
   		for journal_url in 200journal:
   			crawl_site(journal_url)
   		n+=200

def crawl_url_conference(url):
	webpage = requests.get (url)
	tree = html.fromstring(webpage.content)
	conference = tree.xpath('//div[@id="browse-conf-output"]/div[@class="hide-body"]/ul/li/a/@href')
	conference_url =[]
	for conference_url in conference:
		conference_url.append(conference_url)
	return conference_url
	n = 1
    while true:
   		200conference=crawl_url_conference('http://dblp.uni-trier.de/db/conf/?pos=' + n)
   		for conference_url in 200conference:
   			crawl_site(conference_url)
   		n+=200





