from contextlib import contextmanager
import re


class FileSearcher(object):

    def __init__(self, filename, regexp_str):
        self.filename = filename
        self.regexp = re.compile(regexp_str)

    @contextmanager
    def open_file(self):
        with open(self.filename, "rb") as f:
            yield f

    def find_matches(self):
        with self.open_file() as f:
            results = {}
            for i, line in enumerate(f):
                matchobj = self.regexp.match(line)
                if matchobj:
                    results[i] = line
            return results
