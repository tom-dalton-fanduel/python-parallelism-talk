import logging
import threading

from .plotter import FractalPlotter


LOG = logging.getLogger(__name__)


class ThreadedFractalPlotter(FractalPlotter):

    def render(self):
        threads = []
        for x in self._iterate_x_lines():
            line_thread = threading.Thread(
                target=self._render_x_line,
                args=(x, ),
            )
            threads.append(line_thread)
            line_thread.start()

        for t in threads:
            t.join()
