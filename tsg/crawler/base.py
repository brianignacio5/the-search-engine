from lxml import html
import requests
import re
import os
import logging
import validators
from tsg import config
from tsg.crawler.downloader import get_site
from tsg.robots_parser import parse_robots


def crawl_site(url, category):
    logging.info('Downloading URL site {}'.format(url))
    url_parts = re.search('([^/]*)/([^/]*)$', url).groups()
    filename = '{}_{}_{}{}'.format(category,
                                   url_parts[0],
                                   url_parts[1],
                                   '' if url_parts[1][-5:] == '.html'
                                   else'.html')

    doc_path = config.RAW_DIR + filename
    if os.path.isfile(doc_path):
        logging.warn('File {} exists already. Skipping'.format(doc_path))
        return

    try:
        webpage = get_site(url)
        with open(doc_path, 'w') as f:
            f.write(webpage.text)
            logging.info('File at {}'.format(doc_path))
    except requests.exceptions.HTTPError:
        pass


def crawl_journal_url(journal_url):
    logging.info('Downloading URL {}'.format(journal_url))
    journal_site = get_site(journal_url)
    tree = html.fromstring(journal_site.content)
    journal_info_links = tree.xpath("//div[@id='main']/p/a/@href")
    journal_volume_links = tree.xpath("//div[@id='main']/ul/li/a/@href")

    for i, volume in enumerate(journal_volume_links):
        if not validators.url(volume):
            logging.info('Fixing url {}'.format(journal_url))
            journal_volume_links[i] = journal_url + '/' + volume

    journal_links = [journal_info_links,journal_volume_links]
    return journal_links

def crawl_conference_url(conference_url):
    """ Crawl URLs for conference details

    """
    logging.info('Downloading URL {}'.format(conference_url))
    conference_site = get_site(conference_url)
    tree = html.fromstring(conference_site.content)
    conference_details_urls = \
        tree.xpath('//div[@class="data"]/a[text()="[contents]"]/@href')
    return conference_details_urls


def crawl_journal_subsites(journal_url):
    logging.info('Crawling journal volumes in {}'.format(journal_url))
    journal_links = crawl_journal_url(journal_url)
    for journal_volume_site in journal_links[1]:
        crawl_site(journal_volume_site,'journal')


def crawl_conference_subsites(conference_url):
    logging.info('Crawling conference details in {}'.format(conference_url))
    conference_links = crawl_conference_url(conference_url)
    for conference_details_url in conference_links:
        crawl_site(conference_details_url, 'conference')

def crawl_urls(url):
    logging.info('Downloading URL {}'.format(url))
    webpage = get_site(url)
    tree = html.fromstring(webpage.content)
    links = tree.xpath("//div[contains(@id,'output')]//ul/li/a/@href")
    return links


def crawl_loop(category, n=1):
    robots_file = get_site('http://dblp.uni-trier.de/robots.txt')
    config.THROTTLE_SECONDS, config.ALLOWED_SITES, config.DISALLOWED_SITES = \
        parse_robots(robots_file.text)

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

    while True:
        links = crawl_urls(url.format(str(n)))
        if len(links) < 1:
            logging.warn('Didn\' find any links')
            break
        for link in links:
            if category == 'journal':
                crawl_journal_subsites(link)
            elif category == 'conference':
                crawl_site(link, category)
                crawl_conference_subsites(link)
            else:
                crawl_site(link, category)
        n += pagination
    return n
