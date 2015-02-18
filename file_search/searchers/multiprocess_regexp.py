import logging
from multiprocessing import Manager, Pool, Process, Queue

from .searcher import FileSearcher


LOG = logging.getLogger(__name__)


def queue_matches(regexp, queue, line_offset, block):
    for i, line in enumerate(block):
        matchobj = regexp.match(line)
        if matchobj:
            queue.put((line_offset + i, line, ))
    queue.put(None)


def enqueue_blocks(filename, q, block_size=1 * 1000 * 1000):
    block = []
    next_item = (0, block, )
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            block.append(line)

            if len(block) == block_size + 1:
                q.put(next_item)
                block = []
                next_item = (i + 1, block, )

    # Any remaining lines
    if block:
        q.put(next_item)

    LOG.info("Finished queueing file data blocks")
    q.put(None)


class MultiprocessRegexpFileSearcher(FileSearcher):

    def find_matches(self):
        block_queue = Queue()
        LOG.info("Starting file reader")
        file_reader_process = Process(
            target=enqueue_blocks,
            args=(self.filename, block_queue, ),
        )
        file_reader_process.start()

        LOG.info("Starting regexp workers")
        m = Manager()
        results_queue = m.Queue()
        regexp_process_pool = Pool(32)
        num_workers = 0
        while True:
            next_item = block_queue.get()
            if next_item is None:
                break

            line_offset, block = next_item
            LOG.info("Apply_async worker job {}".format(num_workers))
            regexp_process_pool.apply_async(
                queue_matches,
                (self.regexp, results_queue, line_offset, block, ),
            )
            num_workers += 1

        regexp_process_pool.close()

        results = {}
        num_finished = 0
        while num_finished < num_workers:
            item = results_queue.get()
            if item is None:
                num_finished += 1
            else:
                line_num, line = item
                results[line_num] = line

        file_reader_process.join()
        regexp_process_pool.join()

        return results
