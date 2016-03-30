from lxml import html
import re
import os
import logging
from tsg.config import RAW_DIR
from tsg.crawler.downloader import get_site


def crawl_site(url, category):
    logging.info('Downloading URL {}'.format(url))
    url_parts = re.search('([^/]*)/([^/]*)$', url).groups()
    filename = '{}_{}_{}{}'.format(category,
                                   url_parts[0],
                                   url_parts[1],
                                   '' if url_parts[1][-5:] == '.html'
                                   else'.html')

    doc_path = RAW_DIR + filename
    if os.path.isfile(doc_path):
        logging.warn('File {} exists already. Skipping'.format(doc_path))
        return

    webpage = get_site(url)
    with open(doc_path, 'w') as f:
        f.write(webpage.text)


def crawl_urls(url):

    logging.info('Downloading URL {}'.format(url))
    webpage = get_site(url)
    tree = html.fromstring(webpage.content)
    links = tree.xpath("//div[contains(@id,'output')]//ul/li/a/@href")
    return links


def crawl_loop(category):

    if category == 'journal':
        url = 'http://dblp.uni-trier.de/db/journals/?pos={}'
        pagination = 100
    elif category == 'author':
        url = 'http://dblp.uni-trier.de/pers?pos={}'
        pagination = 300
    elif category == 'conference':
        url = 'http://dblp.uni-trier.de/db/conf/?pos={}'
        pagination = 100
    else:
        raise ValueError('category must have one of the three!')

    n = 1
    while True:
        links = crawl_urls(url.format(str(n)))
        if len(links) < 1:
            logging.warn('Didn\' find any links')
            break
        for link in links:
            crawl_site(link, category)
        n += pagination
    return n
