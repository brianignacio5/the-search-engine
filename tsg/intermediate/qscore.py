''' Calculate quality score for all documents :)'''
import json
import glob
import numpy as np

def get_distributions(directory):
    # read all documents, get a distribution for q scores
    cats = ['conference_overview', 'conference', 'author', 'journal']
    counts = {cat: [] for cat in cats}

    for filename in glob.glob(directory + '/*.json'):
        with open(filename) as f:
            parsed = json.load(f)
            cat = parsed['type']
            if cat == 'conference' and parsed['url'][-5:] != '.html':
                cat = 'conference_overview'

            counts[cat].append(parsed['listings_count'])


    return {cat: (np.array(counts[cat]).mean(),
                  np.array(counts[cat]).std()) for cat in cats}
