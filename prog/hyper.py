# -*- coding: utf-8 -*-

import numpy as np

import hyperbolic.poincaredisk as disk

pd = disk.instance

o = pd.mkPoint(0, 0)

ratio = 2
limit = 4

xs = []

for x in np.linspace(0.00001, 0.99999, 1000):
    p = pd.mkPoint(x, 0)
    d = pd.distanceBetween(p, o) / ratio
    if d < 0.5 + limit:
        if d - 0.5 >= len(xs):
            xs.append(x)

for x in xs:
    print(x)
    p = pd.mkPoint(x, 1 - x)
    q = pd.mkPoint(x, x - 1)
    r = pd.mkPoint(-x, 1 - x)
    s = pd.mkPoint(-x, x - 1)

    ys = []
    zs = []
    vertical = pd.mkLine(p, q, color='green', linestyle='', marker=',')
    for t in vertical.points():
        d = pd.distanceBetween(t, o) / ratio
        print("* %f" % d)
        if limit - d > len(ys):
            horizatal = vertical.perpendicularAt(t)
            horizatal.plot(pd, color='red', linestyle='', marker=',')
            ys.append(horizatal)
        if len(ys) == limit:
            if limit - d > len(zs):
                horizatal = vertical.perpendicularAt(t)
                horizatal.plot(pd, color='red', linestyle='', marker=',')
                zs.append(horizatal)

    ys = []
    vertical = pd.mkLine(r, s, color='blue', linestyle='', marker=',')
    for t in vertical.points():
        d = pd.distanceBetween(t, o) / ratio
        print("* %f" % d)
        if limit - d > len(ys):
            horizatal = vertical.perpendicularAt(t)
            horizatal.plot(pd, color='red', linestyle='', marker=',')
            ys.append(horizatal)
        if len(ys) == limit:
            if limit - d > len(zs):
                horizatal = vertical.perpendicularAt(t)
                horizatal.plot(pd, color='red', linestyle='', marker=',')
                zs.append(horizatal)

pd.show(block=True)
