import logging
from multiprocessing import Manager, Pool, Process, Queue
import os

from .searcher import FileSearcher


LOG = logging.getLogger(__name__)


def find_matches_in_chunk(
    result_queue,
    filename,
    regexp,
    chunk_offset,
    chunk_limit,
    ignore_first_line=True,
):
    with open(filename, "rb") as f:
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

            matchobj = regexp.match(line)
            if matchobj:
                results[i] = line

            if file_pos > chunk_limit:
                i += 1
                break

        if not results:
            # No data to read from file
            result_queue.put(None)
            return

        result_queue.put((i, results, ))


class MultiprocessFileSearcher(FileSearcher):

    CHUNK_SIZE = 100 * 1024 * 1024
    NUM_PROCESSES = 6

    def num_chunks_needed(self):
        size = os.path.getsize(self.filename)
        if size % self.CHUNK_SIZE == 0:
            # Divides equally, chunks are exactly the right size
            return size / self.CHUNK_SIZE

        # Need an extra chunk to pick up the 'leftovers'
        return (size / self.CHUNK_SIZE) + 1

    def find_matches(self):
        pool = Pool(self.NUM_PROCESSES)
        m = Manager()
        chunks_needed = self.num_chunks_needed()
        result_queues = []
        for i in xrange(chunks_needed):
            result_queue = m.Queue()
            pool.apply_async(
                find_matches_in_chunk,
                kwds={
                    "result_queue": result_queue,
                    "filename": self.filename,
                    "regexp": self.regexp,
                    "chunk_offset": i * self.CHUNK_SIZE,
                    "chunk_limit": (i + 1) * self.CHUNK_SIZE,
                    "ignore_first_line": (i != 0),
                }
            )
            result_queues.append(result_queue)

        pool.close()
        LOG.info("Worker pool started")

        full_results = {}
        line_count = 0

        for queue in result_queues:
            LOG.info("Waiting for process queue data")
            queue_data = queue.get()
            if queue_data is None:
                continue

            chunk_line_count, results = queue_data
            for chunk_line_num, line in results.iteritems():
                full_results[line_count + chunk_line_num] = line

            line_count += chunk_line_count
            LOG.info("Line count: {}".format(line_count))

        return full_results
