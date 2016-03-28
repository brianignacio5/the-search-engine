#!/usr/bin/env python

import argparse
import logging

from tsg.crawler import crawl_loop

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Crawl one category')
    parser.add_argument('category',
                        choices=['journals', 'authors', 'conferences'])

    args = parser.parse_args()


    crawl_loop(args.category)



if __name__ == "__main__":
    main()
