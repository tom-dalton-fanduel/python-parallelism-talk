import functools
import logging
from multiprocessing import Pool, cpu_count

from .line_plotter import LineFractalPlotter


LOG = logging.getLogger(__name__)


def _callback(line_multiprocess_fractal_plotter, screen_x, x_line_data):
    line_multiprocess_fractal_plotter._render_x_line(screen_x, x_line_data)


class LineMultiprocessFractalPlotter(LineFractalPlotter):

    def _render_x_line(self, x, line_result):
        for y, i in enumerate(line_result):
            self.surface.set_at((x, y, ), self.colouriser.get_colour(i))
        self._update_display_x_line(x)

    def render(self):
        p = Pool(cpu_count())

        for x in self._iterate_x_lines():
            callback = functools.partial(_callback, self, x)
            async_result = p.apply_async(
                self.calc_screen_x_line_func,
                args=(
                    x,
                    self.surf_h,
                    self.surf_scale,
                    self.frac_x0,
                    self.frac_y0,
                    self.max_iterations,
                ),
                callback=callback,
            )

        p.close()
        p.join()
