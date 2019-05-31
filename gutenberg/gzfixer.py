# -*- coding: utf-8 -*-

import glob
import gzip

from sh import cp, rm


counter = 0
normal = 0
for fname in glob.glob('./*/*-*.txt'):
    counter = counter + 1
    try:
        with gzip.open(fname) as g:
            with open('%s.tmp' % fname, 'w+', encoding='utf-8') as o:
                for l in g.readlines():
                    o.write(str(l, 'utf-8'))
            rm(fname)
            cp('%s.tmp' % fname, fname)
            rm('%s.tmp' % fname)
    except Exception as e:
        print(e)
        normal += 1
        rm('%s.tmp' % fname)

print(counter)
print(normal)
