from tsg.crawler import crawl_site, crawl_urls
import os
import requests
from tsg.config import RAW_DIR


def test_crawl_urls():
    url = 'http://dblp.uni-trier.de/pers?pos=1'
    urls = crawl_urls(url)
    assert len(urls) == 300
    assert urls[:2] == ['http://dblp.uni-trier.de/pers/hd/a/A:Almaaf_Bader_Ali',
                        'http://dblp.uni-trier.de/pers/hd/a/A:Ambha']
    assert urls[-1] == 'http://dblp.uni-trier.de/pers/hd/a/Aaltonen:Viljakaisa'

    #  TODO: do the test for journals and conferences as well


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
