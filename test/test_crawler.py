from tsg.crawler import crawl_site, crawl_urls, crawl_journal
import os
import requests
from tsg.config import RAW_DIR

def test_crawl_journal():
    url = 'http://dblp.uni-trier.de/db/journals/crossroads/'
    url_journals = crawl_journal(url)
    assert url_journals[0][:2] == ['http://xrds.acm.org',
                                'http://dl.acm.org/citation.cfm?id=J1271']
    assert url_journals[1][:2] == ['http://dblp.uni-trier.de/db/journals/crossroads/crossroads22.html',
                                    'http://dblp.uni-trier.de/db/journals/crossroads/crossroads21.html']

def test_crawl_urls():
    url = 'http://dblp.uni-trier.de/pers?pos=1'
    urls = crawl_urls(url)
    assert len(urls) == 300
    assert urls[:2] == ['http://dblp.uni-trier.de/pers/hd/a/A:Almaaf_Bader_Ali',
                        'http://dblp.uni-trier.de/pers/hd/a/A:Ambha']
    assert urls[-1] == 'http://dblp.uni-trier.de/pers/hd/a/Aaltonen:Viljakaisa'

    #Journals
    url_journals = 'http://dblp.uni-trier.de/db/journals/?pos=1'
    url_journals = crawl_urls(url_journals)
    print(url_journals[:2])
    assert len(url_journals) == 100
    assert url_journals[:2] == ['http://dblp.uni-trier.de/db/journals/ij3dim',
                                'http://dblp.uni-trier.de/db/journals/4or']
    assert url_journals[-1] == 'http://dblp.uni-trier.de/db/journals/jaif'

    # Conferences
    url_conferences = 'http://dblp.uni-trier.de/db/conf/?pos=1'
    url_conferences = crawl_urls(url_conferences)
    assert len(url_conferences) == 100

    assert url_conferences[:2] == ['http://dblp.uni-trier.de/db/conf/3dpvt',
                                    'http://dblp.uni-trier.de/db/conf/3dgis']
    assert url_conferences[-1] == 'http://dblp.uni-trier.de/db/conf/ACMse'

def test_crawl_site():
    url = 'http://dblp.uni-trier.de/pers/hd/w/Walker:David'
    filename = RAW_DIR + 'author_w_Walker:David.html'

    assert not os.path.exists(filename)

    crawl_site(url, 'author')

    webpage = requests.get(url)

    assert os.path.exists(filename)
    with open(filename) as f:
        assert f.read() == webpage.text


def test_crawl_site_html_suffix():
    url = 'http://dblp.uni-trier.de/db/journals/tap/tap7.html'
    filename = RAW_DIR + 'journal_tap_tap7.html'

    assert not os.path.exists(filename)

    crawl_site(url, 'journal')

    webpage = requests.get(url)

    assert os.path.exists(filename)
    with open(filename) as f:
        assert f.read() == webpage.text
