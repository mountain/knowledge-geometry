# -*- coding: utf-8 -*-

import numpy as np

cum = 1
p = 1 - 1 / np.e
for i in range(1000):
    xs = - np.arange(i + 1)
    r = p * np.sum(np.exp(xs))
    cum *= r
    print(i, xs[i], r, cum)
print(cum)
print(p)
