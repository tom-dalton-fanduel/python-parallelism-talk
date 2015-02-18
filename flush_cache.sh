#!/bin/sh
# Flush the disk cache to make IO-based benchmarks repeatable

echo "Pre-flush stats:"
free
echo "Flushing/clearing"
sudo sync
sudo sh -c 'echo 3 >/proc/sys/vm/drop_caches'
echo "Current stats:"
free

