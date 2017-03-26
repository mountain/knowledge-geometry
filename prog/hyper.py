# -*- coding: utf-8 -*-

import hyperbolic.poincaredisk as disk

pd = disk.instance

pd.mkBoundary()

p0 = pd.mkPoint(0.1, 0.2)
pp1 = pd.mkPoint(0.1, 0.1)

l1 = pd.mkLine(p0, pp1, color='green', linestyle='', marker=',')

pd.show(block=True)
