def calc_point(x0, y0, max_iterations):
    """Return None or a divergence speed [0.0,1.0)."""

    x = 0.0
    y = 0.0
    for i in xrange(max_iterations):
        if x * x + y * y >= 4.0:
            # Diverging
            return i

        x_temp = x * x - y * y + x0
        y = 2 * x * y + y0
        x = x_temp

    # Didn't divege
    return None


def calc_screen_x_line(
        screen_x, screen_h, screen_scale, frac_x0, frac_y0, max_iterations):

    points = []
    frac_x = frac_x0 + (screen_x / screen_scale)
    for screen_y in xrange(screen_h):
        frac_y = frac_y0 + (screen_y / screen_scale)
        points.append(calc_point(frac_x, frac_y, max_iterations))
    return points
