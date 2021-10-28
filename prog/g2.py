import sys

from PIL import Image
from numpy import array, dot, cross, inf, linspace
from numpy.linalg import solve
from math import cos, sin, sqrt, pi
from fractions import Fraction

from numpy import seterr

seterr(all='raise')

# utility functions

width = 4097
coord = linspace(-1, 1, num=width)


def refl(vector, mir):
    return vector - 2 * dot(vector, mir) * mir


def unit(vector):
    magnitude = sqrt(abs(dot(vector, vector)))
    return vector / magnitude



pqr = [4, 4]
filestem = "i44"


def mk_mirror(pqr):
    p = pqr.pop(0)
    pangle = pi / p
    cosqr = [-cos(pi / u) for u in pqr]
    while len(cosqr) < 2: cosqr.append(-1)

    v0 = [0, 1, 0]
    v11 = -cos(pangle)
    v12 = sin(pangle)
    v1 = [0, v11, v12]
    v21 = cosqr[0]
    v22 = (cosqr[1] - v11 * v21) / v12
    v2 = [1j * sqrt(abs(1 - v21 ** 2 - v22 ** 2)), v21, v22]
    mirror = [array(v0), array(v1), array(v2)]

    # Move everything so that the origin is equidistant from the mirror.

    omnipoint = unit(solve(array(mirror), array([-0, -64, -0])))
    if omnipoint[0].imag < 0: omnipoint = -omnipoint
    tempmirror = unit(omnipoint - array([1j, 0, 0]))
    for j, u in enumerate(mirror):
        v = refl(u, tempmirror)
        if v[0].imag < 0: v = -v
        mirror[j] = v


mirror = mk_mirror(pqr)
print("mirror", mirror)


def thecolor(x0, x1):
    v0, v1, v2 = mirror
    r2 = x0 ** 2 + x1 ** 2
    if r2 >= 1: return (255, 255, 255, 0)

    bottom = 1 - r2
    p = array([1j * (1 + r2) / bottom, 2 * x0 / bottom, 2 * x1 / bottom])

    clean = 0
    while True:
        for j, u in enumerate(mirror):
            if dot(p, u) > 0:
                p = refl(p, u)
                clean = 0
            else:
                clean += 1
                if clean >= 3:
                    # 1:
                    if abs(dot(p, v0)) < 0.02: return (0, 0, 255, 255)
                    return (255, 0, 0, 255)


im = Image.new("RGBA", (width, width))
im.putdata([thecolor(x, y)
            for y in coord
            for x in coord
            ])
im.save("%s.png" % (filestem))
