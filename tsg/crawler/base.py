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

def crawl_authors():
    n = 1
    authors300 = []
    while True:
        authors300 = crawl_urls("http://dblp.uni-trier.de/pers?pos=" + str(n))
        if len(authors300) < 1:
            break
        for author in authors300:
            crawl_site(author)
        n += 300
        return n

