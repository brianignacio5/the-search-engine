# the-search-engine
Website crawler and attached search engine for the results.

## Testing

Is done with Nose
https://www.google.de/search?q=python+nosetests&gws_rd=ssl

## Later - Things to do later

Instead of having different indexes, we can just multiply the number of occurences of a word by n(say 4) if it appears in a title to boost the title's weight.

### word preprocessing

In the parser, change words like "writing" to "writ" so if a user searches for "write", it will be found (by converting it as well to "writ").
Also possible to tweak on -: "Hola WHATS-up" -> "hola whats up whatsup whats-up"

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

## Parts of the search engine

### Web Crawler

In charge of crawling the websites html files in a filedirectory in the server.

#### Web crawler elements of design.


### Parser

In charge of parsing the raw input text, outputting structed terms, usable by the intermediate.

###intermediate or Indexer

Builds intermediate lists to be used by the indexer in the following form (or different):

term1: { set of docs with number of ocurrences in each doc } example: doc1:3, doc4:6, ...
term2: ...
...

### Indexer

In charge of building a term dictionary or index based on documents links, term frequencies and documents frequencies. hero lists/tier-based lists.


####Ideas of indexes to build


Keep additional fields/indexes for each term:

* Title
* ISBN
* Type (Conference, Journal, Author),
* Content(for additional ranking)

On query search, search all these indexes separately and combine results.

### Query Parser

Based on the query, run an algorithm which looks in indexes the relevant results.

- tf-idf!
- Ordering importance (different indexes have different weights)
  - Match title first
  - Match body later
- Semantic scoring based on query
  - Relation between requested term and for example a conference to improve scoring. <- Difficult!

#### Example

Search for

"watch" finds

doc1 and doc3 in index 'body' with tf-idf weights 2.3 and 0.7 respectively, and doc3 in index 'title' with tf-idf 1. We assign (hard-coded) an amplifier for the title index of 2.0, ISBN of 3.0 and Type of 2.5.

Now we combine the results of all the index search, suming up the amplified weights so we get as a final result-list:

[doc3:2.7, doc1:2.3]

