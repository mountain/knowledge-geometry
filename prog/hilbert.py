# -*- coding: utf-8 -*-

import numpy as np

import hilbertcurve.hilbertcurve as hc

from pyx import *


def trnas(x, y, r):
    x = x - r
    y = y - r
    return r + x * np.sqrt(r * r - y * y / 2), r + y * np.sqrt(r * r - x * x / 2)


def drawHilbertSquare(points, fname):
    c = canvas.canvas()

    paths = []
    for ix, pts in enumerate(points):
        x, y = pts
        if ix == 0:
            paths.append(path.moveto(x, y))
        else:
            paths.append(path.lineto(x, y))
            paths.append(path.moveto(x, y))

    hilbert = path.path(*paths)
    c.stroke(hilbert, [style.linewidth.thin])
    c.writeEPSfile(fname)


def drawHilbertDisk(points, fname):
    c = canvas.canvas()

    paths = []
    radius = np.max(points) / 2
    for ix, pts in enumerate(points):
        x, y = pts
        if ix == 0:
            u, v = trnas(x, y, radius)
            paths.append(path.moveto(u, v))
            x0, y0 = x, y
        else:
            for t in range(17):
                xt = x0 + (x - x0) / 16 * t
                yt = y0 + (y - y0) / 16 * t
                ut, vt = trnas(xt, yt, radius)
                paths.append(path.lineto(ut, vt))
                paths.append(path.moveto(ut, vt))
            x0, y0 = x, y

    hilbert = path.path(*paths)
    c.stroke(hilbert, [style.linewidth.thin])
    c.writeEPSfile(fname)


for ii in range(5):
    curve = hc.HilbertCurve(ii + 2, 2)
    width = 2 ** ii
    points = curve.points_from_distances(np.arange(4 * (2 ** ii) ** 2))
    drawHilbertSquare(points, "./images/hilbertsq%s.eps" % ii)
    drawHilbertDisk(points, "./images/hilbertcc%s.eps" % ii)
