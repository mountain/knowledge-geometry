# -*- coding: utf-8 -*-

import numpy as np
import hyperbolic.poincaredisk as disk
import matplotlib.pyplot as plt


cmap = plt.get_cmap('tab10')


pd = disk.instance

phi = np.pi / 3
s = np.sin([phi])[0]
c = np.cos([phi])[0]

p = pd.mkPoint(c, s)
n = pd.mkPoint(0, -1)
h = pd.mkLine(p, n, color='red', linestyle='', marker=',')
l = list(h.points())
o = l[len(l) // 2]

flag = True
counter = 2


def find(p, dirct, length, limit):
    global flag, counter
    for q in dirct.points():
        d = pd.distanceBetween(p, q)
        if flag and length - limit < d < length + limit:
            yield q
            flag = False
            counter -= 1
        if counter == 1 and not flag and (length - limit > d or d > length + limit):
            flag = True
        if counter == 0:
            counter = 2


def gen(depth, start, dirct):
    if depth < 10:
        for point in find(start, dirct, 1.648, 0.008):
            pd.mkLine(start, point, color=cmap(depth), linestyle='', marker=',')
            gen(depth + 1, point, dirct.perpendicularAt(point))


gen(0, o, h)
pd.show(block=True)
