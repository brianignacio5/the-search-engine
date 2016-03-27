import re
import json
import uuid

from lxml import etree


def extract_content(input_file):
    main_xpath = '//div[@id="main"]//text()'
    title_xpath = '//h1/text()'

    parser = etree.HTMLParser()
    tree = etree.parse(input_file, parser)
    words = " ".join(tree.xpath(main_xpath))
    title = tree.xpath(title_xpath)[0]
    return title, words.replace('\xa0', ' ')


def parse_text(unparsed):
    lowered = unparsed.lower().replace('-', ' ')
    parsed = re.sub('[^\w ]', '', lowered)
    parsed = re.sub(' {2,}', ' ', parsed)
    return parsed.strip()


def parse_document(document_type, input_path, output_path):
    title, words = extract_content(input_path)
    parsed = parse_text(words)
    data = {
        'isbn': '',
        'content': parsed,
        'title': title,
        'uuid': str(uuid.uuid4()),
        'type': document_type
    }

    with open(output_path, 'w') as output_file:
        json.dump(data, output_file)
