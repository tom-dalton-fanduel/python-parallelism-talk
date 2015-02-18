import re


class FileSearcher(object):

    def __init__(self, filename, regexp_str):
        self.filename = filename
        self.regexp = re.compile(regexp_str)

    def find_matches(self):
        with open(self.filename, "rb") as f:
            results = {}
            for i, line in enumerate(f):
                matchobj = self.regexp.match(line)
                if matchobj:
                    results[i] = line
            return results
