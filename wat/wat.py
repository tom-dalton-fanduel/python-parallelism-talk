#!/usr/bin/env python
from multiprocessing import Process, Queue

def thing(queue, x):
    result = x * 2
    queue.put(result)

q = Queue()
p = Process(target=thing, args=(q, 10, ))

p.start()

p.join()
print q.get()

