TODO

# Query Parser

Take the query, separate by terms, (simplify terms by normalization?), calculate the ranking of query vs docs terms using the following algorithm.

<img src='http://i.imgur.com/W54qpZ3.png'>

Main idea is we already calculated the tf-idf for each term and document, So for each term we find the postings lists, sort by higher tf-idf of each idf term list and return the first K (something to be defined later), save each term list, them find those docs that contains the most number of terms (at least 3 or 4) ordered by higher resulting tf-idf calculated as the sum of all products the query tf-idf and document tf-idf for each term.

