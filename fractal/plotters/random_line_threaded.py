import logging
import random

from .line_threaded import LineThreadedFractalPlotter


LOG = logging.getLogger(__name__)


class RandomLineThreadedFractalPlotter(LineThreadedFractalPlotter):

    def _iterate_x_lines(self):
        x_lines = range(self.surf_w)
        random.shuffle(x_lines)
        return iter(x_lines)
