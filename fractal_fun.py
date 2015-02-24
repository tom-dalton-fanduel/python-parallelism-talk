#!/usr/bin/env python
"""Fun with fractals."""

from collections import OrderedDict
import logging
from argparse import ArgumentParser
import sys
import time

import pygame

from fractal.plotters.line_plotter import LineFractalPlotter
from fractal.plotters.line_multiprocess import LineMultiprocessFractalPlotter
from fractal.plotters.line_threaded import LineThreadedFractalPlotter
from fractal.plotters.multiprocess import MultiprocessFractalPlotter
from fractal.plotters.plotter import FractalPlotter
from fractal.plotters.random_line_multiprocess import RandomLineMultiprocessFractalPlotter
from fractal.plotters.random_line_threaded import RandomLineThreadedFractalPlotter
from fractal.plotters.threaded import ThreadedFractalPlotter


DEFAULT_PLOTTER = "basic"
PLOTTERS = OrderedDict((
    (DEFAULT_PLOTTER, FractalPlotter, ),
    ("line_basic", LineFractalPlotter, ),
    ("threaded", ThreadedFractalPlotter, ),
    ("line_threaded", LineThreadedFractalPlotter, ),
    ("random_line_threaded", RandomLineThreadedFractalPlotter, ),
    ("multiprocess", MultiprocessFractalPlotter, ),
    ("line_multiprocess", LineMultiprocessFractalPlotter, ),
    ("random_line_multiprocess", RandomLineMultiprocessFractalPlotter, ),
))

DISPLAY_SIZE = (1024, 768)
COLOUR_BLACK = (0, 0, 0)

COMMON_FRACTAL_KWARGS = {
    "frac_x0": -2.0,
    "frac_y0": -1.0,
    "frac_y1": 1.0,
    "max_iterations": 20000,
}


def get_args():
    parser = ArgumentParser(description="Plot a fractal.")

    parser.add_argument(
        "--zoom",
        action='store_true',
        default=False,
    )
    parser.add_argument(
        "--quick",
        action='store_true',
        default=False,
    )

    parser.add_argument(
        "--plotter",
        dest="plotters",
        action="append",
        choices=PLOTTERS.keys(),
    )
    parser.add_argument(
        "--all-plotters",
        dest="plotters",
        action="store_const",
        const=PLOTTERS.keys(),
    )

    parser.add_argument(
        "--use-c-extension",
        action="store_true",
        dest="c_extension",
        default=False,
    )

    parser.add_argument(
        "--no-exit",
        action="store_false",
        dest="exit_at_end",
        default=True,
    )

    args = parser.parse_args()
    if not args.plotters:
        parser.print_help()
        sys.exit(1)

    return args


def update_display(*args, **kwargs):
    pygame.display.update(*args, **kwargs)


def main():
    args = get_args()

    logging.basicConfig(level=logging.DEBUG)
    pygame.init()

    _ = pygame.display.set_mode(DISPLAY_SIZE)
    surface = pygame.display.get_surface()

    if args.quick:
        COMMON_FRACTAL_KWARGS["max_iterations"] = 256
    if args.zoom:
        COMMON_FRACTAL_KWARGS["frac_x0"] = -1.18
        COMMON_FRACTAL_KWARGS["frac_y0"] = -0.13
        COMMON_FRACTAL_KWARGS["frac_y1"] = -0.18

    if args.c_extension:
        print "Using C fractal calculator"
        from fractal.fractals.cmandelbrot import (
            calc_point,
            calc_screen_x_line,
        )
    else:
        print "Using pure python fractal calculator"
        from fractal.fractals.mandelbrot import (
            calc_point,
            calc_screen_x_line,
        )

    for plotter_name in args.plotters:
        print "Using {} plotter".format(plotter_name)
        surface.fill(COLOUR_BLACK)
        update_display()

        plotter_class = PLOTTERS[plotter_name]
        plotter = plotter_class(
            surface,
            update_display,
            calc_point,
            calc_screen_x_line,
            **COMMON_FRACTAL_KWARGS
        )
        start = time.time()
        plotter.render()
        end = time.time()
        print "Render took {:.3f} seconds".format(end - start)

    if not args.exit_at_end:
        raw_input("Press enter to exit")

if __name__ == "__main__":
    main()
