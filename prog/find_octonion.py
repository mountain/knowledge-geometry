import itertools as it

from pyoctonion import Octonion


rng = [Octonion(*vals) for vals in list(it.product(range(-1, 2), repeat=8))]
length = len([a for a in rng if a.x_0 + a.x_1 + a.x_2 + a.x_3 + a.x_4 + a.x_5 + a.x_6 + a.x_7 < 3])
total = length * (length - 1) * (length - 2)

idx = 0
for ix, a in enumerate(rng):
    if a.x_0 + a.x_1 + a.x_2 + a.x_3 + a.x_4 + a.x_5 + a.x_6 + a.x_7 < 3:
        for jx, b in enumerate(rng[ix+1:]):
            if b.x_0 + b.x_1 + b.x_2 + b.x_3 + b.x_4 + b.x_5 + b.x_6 + b.x_7 < 3:
                for kx, c in enumerate(rng[(ix+jx+1):]):
                    if c.x_0 + c.x_1 + c.x_2 + c.x_3 + c.x_4 + c.x_5 + c.x_6 + c.x_7 < 3:
                        idx += 1
                        v = a * b * c + b * c + c
                        if v.x_0 == 1 and v.x_1 == 0 and v.x_2 == 0 and v.x_3 == 0 and v.x_4 == 0 and v.x_5 == 0 and v.x_6 == 0 and v.x_7 == 0:
                            print()
                            print(a)
                            print(b)
                            print(c)
                            print(a * b * c + b * c + c)
                            break
                            break
                            break
                        else:
                            if idx % 10000 == 0:
                                print(' %0.5f' % (idx / total * 100), '%')
                            if idx % 100 == 0:
                                print('.', end='')
