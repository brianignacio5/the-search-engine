from tsg.parser import parse_text
from tsg.ranker import rank

from config import DIRECTORY

def search(searchphrase, index_directory):

    parsed_query = parse_text(searchphrase)

    return rank(parsed_query, index_directory)

