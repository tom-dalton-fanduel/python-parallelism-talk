#!/bin/sh

gcc -c -O3 -Wall -Werror -fpic -I/usr/include/python2.7 cmandelbrot.c \
	&& gcc -shared -o cmandelbrot.so cmandelbrot.o \
	&& rm cmandelbrot.o

