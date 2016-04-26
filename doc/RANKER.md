# Ranker

## Input Output
Input = Clean query string
Output = Dictionary with doc IDs as keys and scores as values

### Cosine Score Calculation

1. Split the query by terms and for each term:
  a. Calculate term's query weight
  b. Calculate term-s document weight
  c. Add the product of 2 and 3 to score[doc_id]
  d. Add the square of product of 2 and 3 to length[doc_id]
2. Normalize each score using score[doc_id] = score[doc_id] / length[doc_id]

### Variations
 One can select using AND approach, which resulting docs should include all query terms, a cosine approach
 which would find all docs closer to requested query.

### Page Rank

1. Read Page rank json for doc score. (Path specified in tsg/config.py)

### Quality score
1. The quality score is already included in tf-idf score in indexer phase.




