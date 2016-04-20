import re


def parse_robots(file_content):
    allowed_list, disallowed_list = ([], [])

    for line in file_content.split('\n'):
        matched = re.match('crawl-delay:\s+(.*)', line)
        if matched:
            delay = int(matched.groups()[0])

        matched = re.match('disallow:\s+(.*)', line)
        if matched:
            disallowed_list.append(matched.groups()[0])

        matched = re.match('allow:\s+(.*)', line)
        if matched:
            allowed_list.append(matched.groups()[0])

    return delay, allowed_list, disallowed_list
