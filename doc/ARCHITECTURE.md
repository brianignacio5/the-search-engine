# Architecture

The crawler downloads plain HTML sites with a descriptive title.
The parser, parses these and tokenizes the words, bringing it in a more convenient json format.
The intermediate brings all the tokens in a token: document-list form, so they are easily accessible by the indexer.
The indexer creates the search index from the intermediate data.
...

