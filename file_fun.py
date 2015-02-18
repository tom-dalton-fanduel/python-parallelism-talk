#!/usr/bin/env python
"""How complicated can searching a file relly be?!"""

from argparse import ArgumentParser
from collections import OrderedDict
import logging
import sys
import time

from file_search.searchers.searcher import FileSearcher
from file_search.searchers.multiprocess import MultiprocessFileSearcher
from file_search.searchers.multiprocess_regexp import MultiprocessRegexpFileSearcher
from file_search.searchers.threaded import ThreadedFileSearcher
from file_search.searchers.threaded_regexp import ThreadedRegexpFileSearcher


DEFAULT_SEARCHER = "basic"
SEARCHERS = OrderedDict((
    (DEFAULT_SEARCHER, FileSearcher, ),
    ("threaded", ThreadedFileSearcher, ),
    ("threaded_regexp", ThreadedRegexpFileSearcher, ),
    ("multiprocess", MultiprocessFileSearcher, ),
    ("multiprocess_regexp", MultiprocessRegexpFileSearcher, ),
))


def get_args():
    parser = ArgumentParser(description="Search large files.")

    parser.add_argument(
        "--filename",
    )
    parser.add_argument(
        "--match-re",
        dest="match_re_str",
    )
    parser.add_argument(
        "--searcher",
        choices=SEARCHERS.keys(),
        default=DEFAULT_SEARCHER,
    )

    args = parser.parse_args()

    if not args.filename or not args.match_re_str:
        parser.print_help()
        sys.exit(1)

    return args


def print_results(results):
    for line_number in sorted(results.keys()):
        print "{}: {}".format(
            line_number + 1,
            results[line_number].rstrip(),
        )


def main():
    args = get_args()

    logging.basicConfig(level=logging.DEBUG)

    searcher_class = SEARCHERS[args.searcher]
    searcher = searcher_class(args.filename, args.match_re_str)

    start = time.time()
    results = searcher.find_matches()
    end = time.time()

    print "Search took {:.3f} seconds".format(end - start)
    print "Found {} matching lines".format(len(results))
    #print_results(results)

if __name__ == "__main__":
    main()
