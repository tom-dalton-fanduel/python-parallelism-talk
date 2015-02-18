import functools
import logging
from multiprocessing import Pool, cpu_count

from .plotter import FractalPlotter


LOG = logging.getLogger(__name__)


def _calc_colours_for_point_specs(calc_point_func, point_specs):
    x_line_data = []
    for point_spec in point_specs:
        frac_x, frac_y, iterations = point_spec
        x_line_data.append(calc_point_func(frac_x, frac_y, iterations))
    return x_line_data


def _callback(multiprocess_fractal_plotter, screen_x, x_line_data):
    multiprocess_fractal_plotter._render_x_line(screen_x, x_line_data)


class MultiprocessFractalPlotter(FractalPlotter):

    def _render_x_line(self, x, line_result):
        for y, i in enumerate(line_result):
            self.surface.set_at((x, y, ), self.colouriser.get_colour(i))
        self._update_display_x_line(x)

    def render(self):
        p = Pool(cpu_count())

        for x in self._iterate_x_lines():
            line_point_specs = []
            for y in xrange(self.surf_h):
                frac_coords = list(self.screen_to_frac(x, y))
                line_point_specs.append(frac_coords + [self.max_iterations])

            callback = functools.partial(_callback, self, x)
            calc_colours_for_point_specs = functools.partial(
                _calc_colours_for_point_specs, self.calc_point_func)
            async_result = p.apply_async(
                calc_colours_for_point_specs,
                args=(line_point_specs, ),
                callback=callback,
            )

        p.close()
        p.join()
