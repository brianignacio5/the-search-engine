#!/usr/bin/env python

import argparse
import logging

from tsg.crawler import crawl_loop

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description='Crawl one category')
    parser.add_argument('category',
                        choices=['journal', 'author', 'conference'])

    parser.add_argument('--startnumber', dest='n', default=1, type=int,
                    help='Start crawling from given position instead of one')

    args = parser.parse_args()


    crawl_loop(args.category, args.n)



if __name__ == "__main__":
    main()
