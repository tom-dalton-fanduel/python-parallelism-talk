import logging
from multiprocessing import Manager, Pool

from .searcher import FileSearcher


LOG = logging.getLogger(__name__)


def queue_matches(regexp, queue, line_offset, block):
    results = {}
    for i, line in enumerate(block):
        matchobj = regexp.match(line)
        if matchobj:
            results[line_offset + i] = line
    queue.put(results)


class MultiprocessRegexpFileSearcher(FileSearcher):

    def get_blocks(self, block_size=1000 * 1000):
        block = []
        next_item = (0, block, )
        with open(self.filename, "rb") as f:
            for i, line in enumerate(f):
                block.append(line)

                if len(block) == block_size + 1:
                    yield next_item
                    block = []
                    next_item = (i + 1, block, )

        # Any remaining lines
        if block:
            yield next_item

    def find_matches(self):
        m = Manager()
        result_queues = []
        regexp_process_pool = Pool(8)

        for line_offset, block in self.get_blocks():
            LOG.info("Creating worker job")
            result_queue = m.Queue()
            regexp_process_pool.apply_async(
                queue_matches,
                (self.regexp, result_queue, line_offset, block, ),
            )
            result_queues.append(result_queue)

        regexp_process_pool.close()

        results = {}
        LOG.info("Awaiting results")
        for i, result_queue in enumerate(result_queues):
            worker_results = result_queue.get()
            results.update(worker_results)
            LOG.info("{} worker results received".format(i + 1))

        regexp_process_pool.join()

        return results
