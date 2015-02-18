import functools
import logging
from multiprocessing import Pool, cpu_count
import random

from .line_multiprocess import LineMultiprocessFractalPlotter


LOG = logging.getLogger(__name__)


def _callback(line_multiprocess_fractal_plotter, screen_x, x_line_data):
    line_multiprocess_fractal_plotter._render_x_line(screen_x, x_line_data)


class RandomLineMultiprocessFractalPlotter(LineMultiprocessFractalPlotter):

    def _iterate_x_lines(self):
        x_lines = range(self.surf_w)
        random.shuffle(x_lines)
        return iter(x_lines)
