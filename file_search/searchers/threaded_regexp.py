import logging
from Queue import Queue
import threading

from .searcher import FileSearcher


LOG = logging.getLogger(__name__)


class ThreadedRegexpFileSearcher(FileSearcher):

    def add_matches_to_result(self, results, line_offset, block):
        for i, line in enumerate(block):
            matchobj = self.regexp.match(line)
            if matchobj:
                results[line_offset + i] = line

    def enqueue_blocks(self, q, block_size=10000):
        block = []
        next_item = (0, block, )
        with open(self.filename, "rb") as f:
            for i, line in enumerate(f):
                block.append(line)

                if len(block) == block_size + 1:
                    q.put(next_item)
                    block = []
                    next_item = (i + 1, block, )

        # Any remaining lines
        if block:
            q.put(next_item)

        q.put(None)

    def find_matches(self):
        queue = Queue()
        file_reader_thread = threading.Thread(
            target=self.enqueue_blocks,
            args=(queue, ),
        )
        file_reader_thread.start()

        regexp_threads = []
        results = {}

        while True:
            next_item = queue.get()
            if next_item is None:
                break

            line_offset, block = next_item
            regexp_thread = threading.Thread(
                target=self.add_matches_to_result,
                args=(results, line_offset, block),
            )
            regexp_thread.start()
            regexp_threads.append(regexp_thread)

        file_reader_thread.join()

        for t in regexp_threads:
            t.join()

        return results
