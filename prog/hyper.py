# -*- coding: utf-8 -*-

import hyperbolic.poincaredisk as disk
import math

pd = disk.instance

pd.mkBoundary()

p1 = pd.mkPoint(0.0, 1)
p2 = pd.mkPoint(math.sqrt(0.5), math.sqrt(0.5))

l1 = pd.mkLine(p1, p2)

pd.show(block=True)
