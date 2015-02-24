#!/usr/bin/env python
from multiprocessing import Pool, Queue

def thing(queue, x):
    result = x * 2
    queue.put(result)

q = Queue()
pool = Pool(1)

print pool.apply(thing, (q, 10, ))

