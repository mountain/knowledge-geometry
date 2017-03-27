# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

from numpy import linalg as la


class PoincareDisk:

    def __init__(self):
        fig, ax = plt.subplots(1)
        ax.set_aspect(1)
        self.axis = ax
        self.figure = fig
        self.plt = plt

    def plot(self, shape):
        shape.plot(self)
        plt.show()

    def mkBoundary(self, **xargs):
        b = Boundary()
        b.plot(self, **xargs)
        return b

    def mkPoint(self, u, v, **xargs):
        p = Point(u, v)
        p.plot(self, **xargs)
        return p

    def mkLine(self, p1, p2, **xargs):
        l = Line(p1, p2)
        l.plot(self, **xargs)
        return l

    def distanceBetween(self, o1, o2):
        if o1.kind == 'point' and o2.kind == 'point':
            op2 = o1.x * o1.x + o1.y * o1.y
            oq2 = o2.x * o2.x + o2.y * o2.y
            pq2 = (o1.x - o2.x) * (o1.x - o2.x) + (o1.y - o2.y) * (o1.y - o2.y)
            return np.arccosh(1 + 2 * pq2 / (1 - op2) / (1 - oq2))
        if o1.kind == 'point' and o2.kind == 'line':
            return 0
        if o1.kind == 'line' and o2.kind == 'point':
            return 0
        if o1.kind == 'line' and o2.kind == 'line':
            return 0

    def show(self, **xargs):
        self.plt.show(**xargs)


class Boundary:

    def __init__(self):
        self.kind = 'boundary'
        self.t = np.linspace(0, 2 * np.pi, 1000)
        self.x = np.cos(self.t)
        self.y = np.sin(self.t)

    def plot(self, pd, **xargs):
        pd.axis.plot(self.x, self.y, **xargs)


class Point:

    def __init__(self, x, y):
        self.kind = 'point'
        self.x = np.array([x])
        self.y = np.array([y])

    def plot(self, pd, **xargs):
        pd.axis.plot(self.x, self.y, **xargs)


class Line:

    def __init__(self, u, v):
        self.kind = 'line'

        centerx = 0.0
        centery = 0.0
        radius = 1.0
        if u.kind == 'point' and v.kind == 'point':
            ux = np.array(u.x)
            uy = np.array(u.y)
            vx = np.array(v.x)
            vy = np.array(v.y)
            a = (uy * (vx * vx + vy * vy) - vy * (ux * ux + uy * uy) + uy - vy) / (2 * (ux * vy - uy * vx))
            b = (vx * (uy * uy + ux * ux) - ux * (vy * vy + vx * vx) + vx - ux) / (2 * (ux * vy - uy * vx))
            centerx = -a
            centery = -b
            radius = math.sqrt(a * a + b * b - 1)
            self.qform = np.array([[1, 0, a],
                                   [0, 1, b],
                                   [a, b, 1]])
            self.det = la.det(self.qform)
            self.eigvals, self.eigvecs = la.eig(self.qform)

        if u.kind == 'line' and v.kind == 'point':
            pass

        self.centerx = centerx
        self.centery = centery
        self.radius  = radius
        self.t = np.linspace(0, 2 * np.pi, 1000 * self.radius)
        self.x = self.centerx + self.radius * np.cos(self.t)
        self.y = self.centery + self.radius * np.sin(self.t)
        self.r = self.x ** 2 + self.y ** 2
        self.x = self.x * (self.r < 1)
        self.y = self.y * (self.r < 1)

    def plot(self, pd, **xargs):
        pd.axis.plot(self.x, self.y, **xargs)

    def ideals(self):
        self.kind = 'line'

instance = PoincareDisk()