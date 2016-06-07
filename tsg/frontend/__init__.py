from functools import wraps
import logging

from flask import request, Response, Flask, jsonify

from tsg.search import search
from tsg.config import DICTIONARY_PATH, INDEXINFO_PATH


app = Flask(__name__)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    # no worries if this is on GH for now..
    return username == 'admin' and password == 'brianmoritzmiguel'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/search')
@requires_auth
def api_search():
    query = request.args.get('query', '')
    logging.info('Searching for \'{}\''.format(query))
    results = search(query, DICTIONARY_PATH, INDEXINFO_PATH)
    return jsonify(results=results)
