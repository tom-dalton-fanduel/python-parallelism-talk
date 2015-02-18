class IterationColouriser(object):

    """Convert numbers into colours!"""

    COLOUR_SCALE = 256

    def __init__(self):
        self.bands = (
            self._blue_green,
            self._green_yellow,
            self._yellow_orange,
            self._orange_red,
            self._red_purple,
        )

    def _clip_float_to_int(self, value):
        scaled = int(value * self.COLOUR_SCALE)
        return max(0, min(scaled, self.COLOUR_SCALE - 1))

    def _scale_colour(self, colour):
        return tuple(self._clip_float_to_int(value) for value in colour)

    def _blue_green(self, x):
        return (0, x, 1.0 - x, )

    def _green_yellow(self, x):
        return (x, 1.0, 0.0, )

    def _yellow_orange(self, x):
        return (1.0, 1.0 - (x / 2), 0.0, )

    def _orange_red(self, x):
        return (1.0, 0.5 - (x / 2), 0.0, )

    def _red_purple(self, x):
        return (1.0, 0.0, x, )

    def get_colour(self, i):
        """Return an appropriate colour for an iteration number.

        This will cycle through the full colour band for an input in the range
        of 0-255.

        If x is None return black.

        """
        if i is None:
            return (0, 0, 0, )

        # Normalise the number to the range of [0,1)
        x = (i / 256.0) % 1

        num_bands = len(self.bands)
        for band_idx, band_func in enumerate(self.bands):
            if int(x * num_bands) < band_idx + 1:
                norm = num_bands * (x - float(band_idx) / num_bands)
                colour = band_func(norm)
                return self._scale_colour(colour)

        # Ran off the end of the bands
        raise Exception(x)
