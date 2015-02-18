#include <Python.h>


int _calc_point(double x0, double y0, int max_iterations) {
	int i;
	double x_temp;
	double x = 0.0;
	double y = 0.0;

	for (i=0; i < max_iterations; i++) {
        	if (x * x + y * y >= 4.0) {
        		// Diverging
			return i;
		}
	        x_temp = x * x - y * y + x0;
	        y = 2 * x * y + y0;
	        x = x_temp;
	}
	return -1;
}


static PyObject * calc_point(PyObject *self, PyObject *args) {
	double x0;
	double y0;
	int max_iterations;

	int i;

	if (!PyArg_ParseTuple(args, "ddi", &x0, &y0, &max_iterations)) {
        	return NULL;
	}

	Py_BEGIN_ALLOW_THREADS;
	i = _calc_point(x0, y0, max_iterations);
	Py_END_ALLOW_THREADS;

	if (i == -1) {
		Py_RETURN_NONE;
	} else {
		return Py_BuildValue("i", i);
	}		
};


static PyObject * calc_screen_x_line(PyObject *self, PyObject *args) {
	int screen_x, screen_h, max_iterations;
	double screen_scale, frac_x0, frac_y0;

	int screen_y;
	double frac_x, frac_y;
	int * c_results;
	PyObject * python_results;

	if (!PyArg_ParseTuple(args, "iidddi", &screen_x, &screen_h, &screen_scale, &frac_x0, &frac_y0, &max_iterations)) {
        	return NULL;
	}

	Py_BEGIN_ALLOW_THREADS;

	c_results = malloc(screen_h * sizeof(int));
	frac_x = frac_x0 + ((double)screen_x / screen_scale);

	for (screen_y=0; screen_y<screen_h; screen_y++) {
		frac_y = frac_y0 + ((double)screen_y / screen_scale);
		c_results[screen_y] = _calc_point(frac_x, frac_y, max_iterations);
	}

	Py_END_ALLOW_THREADS;

	python_results = PyTuple_New(screen_h);
	for (screen_y=0; screen_y<screen_h; screen_y++) {
		if (c_results[screen_y] == -1) {
			Py_INCREF(Py_None);
			PyTuple_SetItem(python_results, screen_y, Py_None);
		} else {
			PyTuple_SetItem(python_results, screen_y, Py_BuildValue("i", c_results[screen_y]));
		}
	}
	free(c_results);
	return python_results;
}


static PyMethodDef c_mandelbrot_methods[] = {
	{"calc_point",  calc_point, METH_VARARGS, "Calculate a point on a mandelbrot fractal."},
	{"calc_screen_x_line",  calc_screen_x_line, METH_VARARGS, "Calculate a whole line (for given x) of points on a mandelbrot fractal."},
	{NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC initcmandelbrot(void)
{
	(void) Py_InitModule("cmandelbrot", c_mandelbrot_methods);
};
