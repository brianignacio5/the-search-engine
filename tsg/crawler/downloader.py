import logging
import requests
import time
import datetime

from tsg.config import THROTTLE_SECONDS


def get_site(url):
    """Crawls site and checks for error. Waits if necessary

    :url: The url to crawl
    :returns: The website object returned by requests.get

    """

    while True:
        wait_time = THROTTLE_SECONDS - \
            (datetime.datetime.now().timestamp()-get_site.last_call)
        if wait_time > 0:
            time.sleep(wait_time)
        result = requests.get(url)
        get_site.last_call = datetime.datetime.now().timestamp()

        if result.status_code != 200:
            logging.warn('There was a problem getting URL {}: Status code: {}'.
                         format(url, result.status_code))

            if result.status_code == 404:
                return result

            if result.status_code == 429:
                retry_after = int(result.headers['retry-after'])
                logging.info('Waiting for {} seconds'.format(
                    retry_after
                ))
                print('Waiting now. Press Control+C to go on before the timout')
                try:
                    time.sleep(retry_after)
                except KeyboardInterrupt:
                    pass
        else:
            return result
get_site.last_call = datetime.datetime.now().timestamp()
