# -*- coding: utf-8 -*-

import hyperbolic.poincaredisk as disk
import math

pd = disk.instance

pd.mkBoundary()

p0 = pd.mkPoint(0.0, 0.0)
p1 = pd.mkPoint(0.0, 1.0)
p2 = pd.mkPoint(1.0, 0.0)

l1 = pd.mkLine(p1, p2)

pd.show(block=True)
