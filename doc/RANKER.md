# Ranker

## Input Output
Input = Clean query string
Output = Dictionary with doc IDs as keys and scores as values

## Workflow

### Cosine Score Calculation

1. Split the query by terms and for each term:
  a. Calculate term's query weight
  b. Calculate term-s document weight
  c. Add the product of 2 and 3 to score[doc_id]
  d. Add the square of product of 2 and 3 to length[doc_id]
2. Normalize each score using score[doc_id] = score[doc_id] / length[doc_id]


### Page Rank

Add Page Rank (Check page rank algorithms based on links) and PENDING another scoring criteria.




