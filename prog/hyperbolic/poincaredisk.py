# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

from numpy import linalg as la


class PoincareDisk:

    def __init__(self):
        fig, ax = plt.subplots(1, 1)
        ax.set_aspect(1)
        self.axis = ax
        self.figure = fig
        self.plt = plt
        self.figure.set_size_inches(7.5, 7.5)
        self.plt.axis('off')
        self.axis.set_xlim([-1.01, 1.01])
        self.axis.set_ylim([-1.01, 1.01])

        self.boundary = self.mkBoundary()

    def plot(self, shape):
        shape.plot(self)
        self.plt.show()
        mng = self.plt.get_current_fig_manager()
        mng.frame.Maximize(True)

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

    def reflectX(self, p):
        if p.kind == 'point':
            q = Point()
            op = np.mat([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
            m = op.dot(p.to_weierstrass())
            q.from_weierstrass(m)
            return q

    def reflectB(self, p, d):
        if p.kind == 'point':
            q = Point()
            op = np.mat([[-np.cosh(2 * d), 0, np.sinh(2 * d)], [0, 1, 0], [-np.sinh(2 * d), 0, np.cosh(2 * d)]])
            m = op.dot(p.to_weierstrass())
            q.from_weierstrass(m)
            return q

    def reflectTheta(self, p, theta):
        if p.kind == 'point':
            q = Point()
            op = np.mat([[np.cos(2 * theta), np.sin(2 * theta), 0], [np.sinh(2 * theta), -np.cos(2 * theta), 0], [0, 0, 1] ])
            m = op.dot(p.to_weierstrass())
            q.from_weierstrass(m)
            return q

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

    def points(self):
        for x, y in zip(self.x, self.y):
            yield Point(x, y, visible=False)


instance = PoincareDisk()


class Point:

    def __init__(self, x, y, visible=False):
        self.kind = 'point'
        self.x = np.array([x])
        self.y = np.array([y])
        self.visible = visible

    def plot(self, pd, **xargs):
        if self.visible:
            pd.axis.plot(self.x, self.y, **xargs)

    def to_weierstrass(self):
        x = self.x
        y = self.y
        p = 1 - x * x - y * y
        q = 1 + x * x + y * y
        return np.array([2 * x / p, 2 * y / p, q / p])

    def from_weierstrass(self, x, y, z):
        self.x = x / (1 + z)
        self.y = y / (1 + z)


class Line:

    def __init__(self, u, v, visible=True):
        self.kind = 'line'
        self.visible = visible

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
        self.radius = radius
        if self.radius > 1000:
            self.radius = 1000
        self.t = np.linspace(0, 2 * np.pi, 1000 * self.radius)
        self.x = self.centerx + self.radius * np.cos(self.t)
        self.y = self.centery + self.radius * np.sin(self.t)
        self.r = self.x ** 2 + self.y ** 2
        self.x = self.x * (self.r < 1)
        self.y = self.y * (self.r < 1)

    def plot(self, pd, **xargs):
        if self.visible:
            pd.axis.plot(self.x, self.y, **xargs)

    def ideals(self):
        self.kind = 'line'

    def perpendicularAt(self, p):
        ux = p.x - self.centerx
        uy = p.y - self.centery

        mn = 1
        s = None
        theta = np.arctan2(self.centerx, self.centery)
        for alpha in np.linspace(-np.pi, np.pi, 1000):
            x = np.cos(alpha + theta)
            y = np.sin(alpha + theta)
            r = Point(x, y)
            l = Line(p, r, visible=False)
            vx = p.x - l.centerx
            vy = p.y - l.centery
            test = np.abs(ux * vx + uy * vy) / np.sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
            if mn > test:
                mn = test
                s = r

        print("** %f" % mn)

        return Line(p, s, visible=True)

    def points(self):
        for x, y in zip(self.x, self.y):
            if x != 0 and y != 0:
                yield Point(x, y, visible=False)
