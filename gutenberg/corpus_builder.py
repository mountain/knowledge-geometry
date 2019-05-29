# -*- coding: utf-8 -*-

import codecs
import sys
import numpy as np

from random import sample
from sh import mkdir, wget

byears = []
dyears = []
statuses = []
langs = []
anames = []
forms = []
codes = []

workarea = []
counter = 0
with codecs.open('works.txt', encoding='utf-8') as f:
    for ln in f:
        print('.', end='')
        workarea.append(ln[:-1])
        counter += 1
        if counter % 9 == 0:
            byear, dyear, status, lang, aname, name, form, code, _ = workarea
            assert(_ == '')
            workarea = []
            byears.append(int(byear))
            dyears.append(int(dyear))
            statuses.append(status)
            langs.append(lang)
            anames.append(aname)
            forms.append(form)
            codes.append(code)

        if counter % 80 == 0:
            print('')

used = set()

ix_by = np.argsort(np.array(byears))

for year in range(1600, 2001, 10):
    print('')
    print('%d: ' % year)
    sys.stdout.flush()
    counter = 100
    tries = 0
    indexes = [ix for ix in ix_by if byears[ix] - 100 < year < byears[ix] - 20]
    while counter > 0:
        ixs = sample(indexes, 100)
        for ix in ixs:
            byear = byears[ix]
            dyear = dyears[ix]
            status = statuses[ix]
            lang = langs[ix]
            form = forms[ix]
            aname = anames[ix]
            code = codes[ix]

            cond = byear + 20 < year < dyear and status == 'ok'
            cond = cond and lang == 'English' and form == 'as Author'
            cond = cond and aname not in used
            tries += 1
            if cond:
                if tries % 50 == 0:
                    print('')
                    print('%d: ' % year)
                print('+', end='')
                sys.stdout.flush()

                url = 'https://www.gutenberg.org/ebooks/%s.txt.utf-8' % code
                fname = '%04ds/%04ds-%s.utf8.txt' % (year, year, aname)

                mkdir('-p', '%04ds' % year)
                wget('-O', fname, url)

                used.add(anames[ix])
                counter -= 1
            else:
                if tries % 50 == 0:
                    print('')
                    print('%d: ' % year)
                print('.', end='')
                sys.stdout.flush()
