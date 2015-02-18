import logging

from fractal.plotters.plotter import FractalPlotter


LOG = logging.getLogger(__name__)


class LineFractalPlotter(FractalPlotter):

    def _render_x_line(self, x):
        line_results = self.calc_screen_x_line_func(
            x,
            self.surf_h,
            self.surf_scale,
            self.frac_x0,
            self.frac_y0,
            self.max_iterations,
        )
        for y, iterations in enumerate(line_results):
            colour = self.colouriser.get_colour(iterations)
            self.render_pixel(x, y, colour)
        self._update_display_x_line(x)
