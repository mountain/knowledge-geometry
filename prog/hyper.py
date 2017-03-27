# -*- coding: utf-8 -*-

import numpy as np

import hyperbolic.poincaredisk as disk

pd = disk.instance

pd.mkBoundary()

o = pd.mkPoint(0, 0)

xmap = {}
dmap = {}

i = 0
for x in np.linspace(-1.0, 1.0, 1000):
    p = pd.mkPoint(x, 0)
    d = pd.distanceBetween(p, o)
    if not np.isnan(d) and d < 10:
        D = d * np.sign(x)
        if int(D) not in dmap:
            dmap[int(D)] = d
            xmap[int(D)] = x
        else:
            if dmap[int(D)] > d:
                dmap[int(D)] = d
                xmap[int(D)] = x
    if i % 50 == 0:
        print len(dmap)
    print '.',
    i += 1

print ''

for key in sorted(dmap.keys()):
    x = xmap[key]
    print x
    p = pd.mkPoint(x, 1 - x)
    q = pd.mkPoint(x, x - 1)
    l = pd.mkLine(p, q, color='green', linestyle='', marker=',')

pd.show(block=True)
