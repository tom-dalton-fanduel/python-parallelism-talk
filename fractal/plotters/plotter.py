import logging

from pygame import Rect

from fractal.colours import IterationColouriser
from fractal.fractals.mandelbrot import calc_point


LOG = logging.getLogger(__name__)


class FractalPlotter(object):

    def __init__(
        self,
        surface,
        display_update_callback,
        calc_point_func=None,
        calc_screen_x_line_func=None,
        frac_x0=-2.0,
        frac_y0=-1.0,
        frac_y1=1.0,
        max_iterations=20000,
    ):
        self.surface = surface
        self.colouriser = IterationColouriser()
        self.calc_point_func = calc_point_func
        self.calc_screen_x_line_func = calc_screen_x_line_func
        self.display_update_callback = display_update_callback
        self.frac_x0 = frac_x0
        self.frac_y0 = frac_y0
        self.frac_y1 = frac_y1
        self.max_iterations = max_iterations

        # Screen coords
        self.surf_w, self.surf_h = self.surface.get_size()
        self.surf_scale = self.surf_h / (self.frac_y1 - self.frac_y0)

    def get_colour_for_iterations(self, iterations):
        return self.colouriser.get_colour(iterations)

    def get_iterations_at_point(self, frac_x, frac_y):
        return self.calc_point_func(frac_x, frac_y, self.max_iterations)

    def get_colour_at_point(self, frac_x, frac_y):
        return self.get_colour_for_iterations(
            self.get_iterations_at_point(frac_x, frac_y))

    def screen_to_frac(self, x, y):
        norm_x = x / self.surf_scale
        norm_y = y / self.surf_scale

        return (self.frac_x0 + norm_x, self.frac_y0 + norm_y, )

    def get_pixel_colour(self, x, y):
        frac_coords = self.screen_to_frac(x, y)
        return self.get_colour_at_point(*frac_coords)

    def render_pixel(self, x, y, colour=None):
        if colour is None:
            colour = self.get_pixel_colour(x, y)
        self.surface.set_at((x, y, ), colour)

    def _update_display_x_line(self, x):
        self.display_update_callback(Rect(x, 0, 1, self.surf_h))

    def _render_x_line(self, x):
        for y in xrange(self.surf_h):
            self.render_pixel(x, y)
        self._update_display_x_line(x)

    def _iterate_x_lines(self):
        for x in xrange(self.surf_w):
            yield x

    def render(self):
        for x in self._iterate_x_lines():
            self._render_x_line(x)
