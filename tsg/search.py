from tsg.parser import parse_text
from tsg.ranker import rank

from config import DIRECTORY

def search(searchphrase, index_directory):
    """
    Processes a search query and returns a list of matched documents.

    searchphrase: An unformatted search query
    index_directory: The directory where dictionary.dat and indexinfo.json lie.
    """

    parsed_query = parse_text(searchphrase)

    return rank(parsed_query, index_directory)

