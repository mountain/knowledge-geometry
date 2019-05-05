# -*- coding: utf-8 -*-

import numpy as np
import hyperbolic.poincaredisk as disk


pd = disk.instance
s = np.sin([np.pi / 7])[0]
c = np.cos([np.pi / 7])[0]
o = pd.mkPoint(0, 0)
p = pd.mkPoint(c, s)
n = pd.mkPoint(0, -1)
h = pd.mkLine(p, n, color='green', linestyle='', marker=',')
flag = True


def find(p, dirct, length, limit):
    global flag
    for q in dirct.points():
        check = np.abs([pd.distanceBetween(p, q) - length])
        if flag and np.all(check > limit):
            yield q
            flag = False
        elif not flag and np.all(check < limit):
            yield q
            flag = True


def gen(depth, start, dirct):
    if depth < 2:
        for point in find(start, dirct, np.e, 0.03):
            pd.mkLine(start, point, color='green', linestyle='', marker=',')
            gen(depth + 1, point, dirct.perpendicularAt(point))


gen(0, o, h)
pd.show(block=True)
