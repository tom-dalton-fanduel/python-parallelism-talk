# python-parallelism-talk

This repo contains some demonstration code to support the talk I'm giving to the python-edinburgh group.

The code is horrible and should not be looked at by anyone, ever ;-)

## File Fun

This example is intended to demonstrate parallelising large IO-centric operations.

Note the examples use the flush_cache.sh script to ensure the OS's disk cache doesn't affect the results.

Example:

    ./flush_cache.sh >/dev/null && ./file_fun.py --filename big_sample_file --match-re "^1" --searcher basic

## Fractal Fun

This example is intended to demonstrate parallelising CPU-centric operations.

If you want to use the C extension, you'll probably need to build it first. There is a verison
already included in the repo, but it probably wont work on your system unless you have exactly
the same verison of python.

    cd fractal/ext
    ./build.sh

You'll need pygame installed for this example.

Example (slow):

    ./fractal_fun.py --plotter basic

## Talk Examples

    ./flush_cache.sh >/dev/null && ./file_fun.py --filename big_sample_file --match-re "^1" --searcher basic
