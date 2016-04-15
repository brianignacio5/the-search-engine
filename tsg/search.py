from tsg.parser import parse_text
from tsg.ranker import rank

def search(searchphrase, dictionary_path, indexinfo_path):
    """
    Processes a search query and returns a list of matched documents.

    searchphrase: An unformatted search query
    index_directory: The directory where dictionary.dat and indexinfo.json lie.

    IMPORTANT: Use the dictionary.dat path as index_directory parameter
    until the dictionary hash logic is defined.
    """

    parsed_query = parse_text(searchphrase).split(' ')

    # TODO Modify get_dictionary_term_list in tsg.ranker.base to
    # use the hash dictionary and read a position in dictionary
    # instead of line by line

    return rank(parsed_query, dictionary_path, indexinfo_path)
