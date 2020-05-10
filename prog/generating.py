# -*- coding: utf-8 -*-

import numpy as np

from collections import OrderedDict


class Exp:
    def __init__(self, val=0, gen=1, pth=['0'], bgn=0, end=0, rep=np.array([0], dtype=np.int)):
        self.val = val
        self.gen = gen
        self.pth = pth
        self.bgn = bgn
        self.end = end
        self.rep = np.array(rep)

    def otimes(self):
        gen = self.gen + 1
        val = self.val * np.e
        rep = np.array([0] + list(np.copy(self.rep)))
        bgn = self.bgn
        end = self.end + 1
        pth = self.pth + ['*']
        return Exp(val=val, gen=gen, pth=pth, bgn=bgn, end=end, rep=rep)

    def oslash(self):
        gen = self.gen + 1
        val = self.val / np.e
        rep = np.array(list(np.copy(self.rep)) + [0])
        bgn = self.bgn - 1
        end = self.end
        pth = self.pth + ['/']
        return Exp(val=val, gen=gen, pth=pth, bgn=bgn, end=end, rep=rep)

    def oplus(self):
        gen = self.gen + 1
        val = self.val + 1
        bgn = self.bgn
        end = self.end
        rep = np.copy(self.rep)
        rep[-self.bgn] = rep[-self.bgn] + 1
        pth = self.pth + ['+']
        return Exp(val=val, gen=gen, pth=pth, bgn=bgn, end=end, rep=rep)

    def ominus(self):
        gen = self.gen + 1
        val = self.val - 1
        bgn = self.bgn
        end = self.end
        rep = np.copy(self.rep)
        rep[-self.bgn] = rep[-self.bgn] - 1
        pth = self.pth + ['-']
        return Exp(val=val, gen=gen, pth=pth, bgn=bgn, end=end, rep=rep)

    def validate(self):
        assert len(self.pth) == self.gen
        assert self.bgn <= 0
        assert self.end >= 0
        s = 0
        for ix, ex in enumerate(range(self.bgn, self.end + 1, 1)):
            s += self.rep[ix] * np.exp(ex)
        assert np.abs(self.val - s) <= 0.00001

    def radius(self):
        x, y = 0, 0
        for s in self.pth:
            if s == '+':
                x += 1
            elif s == '-':
                x -= 1
            elif s == '*':
                y += 1
            elif s == '/':
                y -= 1
        return np.abs(x) + np.abs(y)

    def repr(self):
        s = ''
        for ix in range(-self.gen, self.gen, 1):
            if ix < self.bgn:
                s = '+0%s' % s
            elif ix > self.end:
                s = '%s+0' % s
            else:
                s = '%s%+d' % (s, self.rep[ix - self.bgn])
        return s

    def __repr__(self):
        return '%d %s %s %+f' % (self.radius(), ''.join(self.pth), self.repr(), self.val)


generated = [Exp()]
for ix in range(8):
    print('============================')
    print(ix + 1)
    print('----------------------------')
    counter = {}
    unique = {}
    generating = []
    for g in generated:
        for x in [g.oplus(), g.ominus(), g.otimes(), g.oslash()]:
            x.validate()
            generating.append(x)
            #print(x)
            if x.radius() == ix + 1:
                if x.repr() not in counter:
                    counter[x.repr()] = 0
                    unique[x.repr()] = []
                counter[x.repr()] = counter[x.repr()] + 1
                unique[x.repr()].append(x)

    print('----------------------------')
    print('total %d' % len(generating))
    print('unique %d' % len(unique))
    print('all %d' % sum(counter.values()))
    print('residue %d' % (sum(counter.values()) - len(unique)))
    print('----------------------------')
    #for k, v in OrderedDict(sorted(counter.items())).items():
    #    print(k, v)
    #print('----------------------------')

    generated = generating
