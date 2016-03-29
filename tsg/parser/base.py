import re
import json
import uuid
import logging

from lxml import etree

from tsg.config import PARSED_DIR


def extract_content(input_file):
    main_xpath = '//div[@id="main"]//text()'
    title_xpath = '//h1/text()'

    parser = etree.HTMLParser()
    tree = etree.parse(input_file, parser)
    words = " ".join(tree.xpath(main_xpath))
    try:
        title = tree.xpath(title_xpath)[0]
    except IndexError:
        logging.error('File {} doesn\'t seem to have a title'.
                      format(input_file))
        title = ''

    return title, words.replace('\xa0', ' ')


def parse_text(unparsed):
    lowered = unparsed.lower().replace('-', ' ')
    parsed = re.sub('[^\w ]', '', lowered)
    parsed = re.sub(' {2,}', ' ', parsed)
    return parsed.strip()


def parse_document(document_type, input_path):
    title, words = extract_content(input_path)
    parsed = parse_text(words)
    parsed_title = parse_text(title)
    data = {
        'isbn': '',
        'content': parsed,
        'title': parsed_title,
        'uuid': str(uuid.uuid4()),
        'type': document_type
    }
    output_path = '{}{}.json'.format(PARSED_DIR, data['uuid'])
    logging.info('Parsed file {} with uuid {}'.format(input_path, data['uuid']))

    with open(output_path, 'w') as output_file:
        json.dump(data, output_file)
