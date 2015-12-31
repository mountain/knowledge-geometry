# -*- coding: utf-8 -*-

import hyperbolic.poincaredisk as disk


pd = disk.instance

pd.mkBoundary()

p1 = pd.mkPoint(0.0, 0.5, 'ro')
p2 = pd.mkPoint(0.5, 0.5, 'ro')

pd.mkLine(p1, p2, 'yellow')

pd.show()