import logging
import os
from Queue import Queue
import threading

from .searcher import FileSearcher


LOG = logging.getLogger(__name__)


class ThreadedFileSearcher(FileSearcher):

    CHUNK_SIZE = 100 * 1024 * 1024

    def num_chunks_needed(self):
        size = os.path.getsize(self.filename)
        if size % self.CHUNK_SIZE == 0:
            # Divides equally, chunks are exactly the right size
            return size / self.CHUNK_SIZE

        # Need an extra chunk to pick up the 'leftovers'
        return (size / self.CHUNK_SIZE) + 1

    def find_matches_in_chunk(
        self,
        result_queue,
        chunk_offset,
        chunk_limit,
        ignore_first_line=True,
    ):
        with open(self.filename, "rb") as f:
            f.seek(chunk_offset)
            file_pos = chunk_offset
            results = {}

            if ignore_first_line:
                line = f.readline()
                if f.tell() > chunk_limit:
                    # The only line in this chunk started in the previous chunk
                    # and ended in the following chunk. Nothing to do for this
                    # chunk
                    result_queue.put(None)
                    return
                # Ensure the fuile iterator's read ahead buffer is flushed
                # Ref http://stackoverflow.com/questions/14145082/file-tell-inconsistency 
                f.seek(f.tell())
                file_pos += len(line)

            for i, line in enumerate(f):
                if line == "":
                    break

                file_pos += len(line)

                matchobj = self.regexp.match(line)
                if matchobj:
                    results[i] = line

                if file_pos > chunk_limit:
                    # Record current line's existence for the chunk line count
                    i += 1
                    break

            if not results:
                # No data to read from file
                result_queue.put(None)
                return

            result_queue.put((i, results, ))

    def find_matches(self):

        thread_queues = []
        chunks_needed = self.num_chunks_needed()
        LOG.info("Spawning {} chunk-processing threads".format(chunks_needed))
        for i in xrange(chunks_needed):
            queue = Queue()
            thread = threading.Thread(
                target=self.find_matches_in_chunk,
                kwargs={
                    "result_queue": queue,
                    "chunk_offset": i * self.CHUNK_SIZE,
                    "chunk_limit": (i + 1) * self.CHUNK_SIZE,
                    "ignore_first_line": (i != 0),
                }
            )
            thread.start()
            thread_queues.append((thread, queue, ))

        LOG.info("Processing threads started".format(chunks_needed))

        full_results = {}
        line_number = 0

        while thread_queues:
            LOG.info("Waiting for thread")
            thread, queue = thread_queues.pop(0)
            thread.join()
            queue_data = queue.get()
            if queue_data is None:
                LOG.info("Thread found no data - EOF")
            else:
                chunk_line_count, results = queue_data
                for chunk_line_num, line in results.iteritems():
                    full_results[line_number + chunk_line_num] = line

                line_number += chunk_line_count
                LOG.info("Line count: {}".format(line_number + 1))

        return full_results
