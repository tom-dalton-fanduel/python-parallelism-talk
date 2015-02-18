#!/usr/bin/env python

from argparse import ArgumentParser
import progressbar
import random
import string


def get_args():
    parser = ArgumentParser(description="Create large files.")

    parser.add_argument(
        "--min-line-length",
        dest="min_line_length",
        default=10,
    )
    parser.add_argument(
        "--max-line-length",
        dest="max_line_length",
        default=80,
    )

    parser.add_argument(
        "--space-weighting",
        dest="space_weighting",
        default=4,
    )

    parser.add_argument(
        "--num-lines",
        dest="num_lines",
        default=25 * 1000000,
    )

    parser.add_argument(
        "--output-filename",
        dest="output_filename",
        default=generate_filename(),
    )

    args = parser.parse_args()
    return args


def generate_filename():
    return "".join(random.choice(string.ascii_lowercase) for _ in xrange(8))


def generate_line(min_line_length, max_line_length, space_weighting):
    line_length = random.randrange(min_line_length, max_line_length)
    chars = string.ascii_lowercase + (" " * space_weighting)
    return "".join(random.choice(chars) for _ in xrange(line_length)) + "\n"


def main():
    args = get_args()

    with open(args.output_filename, "w") as f:
        pbar = progressbar.ProgressBar(maxval=args.num_lines).start()

        for i in xrange(args.num_lines):
            f.write(generate_line(
                args.min_line_length,
                args.max_line_length,
                args.space_weighting,
            ))
            pbar.update(i)

    print "Created file '{}'".format(args.output_filename)

if __name__ == "__main__":
    main()
