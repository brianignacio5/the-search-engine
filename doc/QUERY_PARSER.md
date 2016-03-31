TODO

# Query Parser

Take query input and pass it to the ranker.

Check if returned number documents is lower than some number, so try different combinations of the query to fill K docs.

Example: "rising interest rates". If < K docs, try "rising interest" and "interest rates" first, fill K docs and if don't fill try "rising interest rates" and fill K docs.
