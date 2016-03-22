# the-search-engine
Website crawler and attached search engine for the results.

## Main Idea so far of search engine workflow

1. Web crawler crawl the website and output file directory with pages.
2. Parser makes a first time list of terms and apply reducing techniques to reduce dictionary.
3. Intermediate build a 2nd time list with parsed terms.
4. Query parser does spell correction and other refining techniques
5. Scoring build score and ranking or terms in index.
  1. matrix for tf-idf scoring to sort documents by relevance.
  2. Intermediate buld scoring of term- conference relationship ratio
  3. Additional Scoring criteria?
6. Returns results in GUI
  1. Define A GUI with text box of query, search button and other advanced search criteria.
  2. Define recall (numbers of docs to return for page)
##Parts of the search engine

###Web Crawler

In charge of crawling the websites html files in a filedirectory in the server.

####Web crawler elements of design.

###Parser

In charge of parsing the terms to adequate for indexing building.

###intermediate or Indexer

In charge of building a term dictionary or index based on documents links, term frequencies and documents frequencies.

####Ideas of indexes to build

1.Keep indexes of titles , ISBN and Body (Content) (Maybe just one big index?)
⋅⋅* Keep additional fields for each term: **Title, ISBN, Type (Conference, Journal, Author), Content** for additional ranking.

###Query Parser

Based on the query, run an algorithm which looks in indexes the relevant results.

1. Ordering importance:
  * Exact matches first, titles match then author match then conferences.
2. Semantic scoring based on query
  * Relation between requested term and for example a conference to improve scoring.


