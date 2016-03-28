# Indexer

Reads the Json files for the terms and creates one line in the dictionary for each of the files/terms (alphabeticaly ordered)

For the beginning ONE index, combining ALL the stuff.

## Dictionary

term1 doc1:tf-idf,doc2:tf-idf   <- ordered by tf-idf
term2 doc5:tf-idf,doc7:tf-idf,..   <- ordered by tf-idf

##  Term Hash

AFTER creating the dictionary, we create a hashfile like this:

term1 byte-position
term2 byte-position

This can be read by the the searcher to find the positions of the terms in the dictionary faster.

## Output

One file with name: dictionary.dat
(second file dictionary_hash.dat) for the dictionary locations.


