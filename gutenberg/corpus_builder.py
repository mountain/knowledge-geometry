# -*- coding: utf-8 -*-

import codecs
import sys
import numpy as np

from random import sample
from sh import mkdir, wget, rm

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
byears = np.array(byears)

ix_by = np.argsort(byears)

for year in range(1600, 2001):
    print('')
    print('%d: ' % year, end='')
    sys.stdout.flush()
    tries = 1
    counter = 3
    decade = year // 10 * 10
    indexes = [ix for ix in ix_by if year - 100 <= byears[ix] <= year - 20]
    while counter >= 1:
        ixs = sample(indexes, 3)

        print('-', end='')
        for ix in ixs:
            if counter >= 1:
                byear = byears[ix]
                dyear = dyears[ix]
                status = statuses[ix]
                lang = langs[ix]
                form = forms[ix]
                aname = anames[ix]
                code = codes[ix]

                cond = byear + 20 <= year <= dyear + 20
                cond = cond and lang == 'English'
                if tries < 1000:
                    cond = cond and aname not in used
                tries += 1
                if cond:
                    fname = '%04ds/%04ds-%06d.txt' % (decade, decade, int(aname[1:]))

                    mkdir('-p', '%04ds' % decade)
                    try:
                        url = 'https://www.gutenberg.org/ebooks/%s.txt.utf-8' % code
                        wget('-O', fname, url)
                        used.add(anames[ix])
                        counter -= 1
                        if tries % 100 == 0:
                            print('')
                            print('%d: ' % year, end='')
                        print('+', end='')
                        sys.stdout.flush()
                    except Exception as e:
                        try:
                            url = 'https://www.gutenberg.org/files/%s/%s-0.txt' % (code, code)
                            wget('-O', fname, url)
                            used.add(anames[ix])
                            counter -= 1
                            if tries % 100 == 0:
                                print('')
                                print('%d: ' % year, end='')
                            print('+', end='')
                            sys.stdout.flush()
                        except Exception as e:
                            if tries % 100 == 0:
                                print('')
                                print('%d: ' % year, end='')
                            print('?', end='')
                            rm('-f', fname)
                else:
                    if tries % 100 == 0:
                        print('')
                        print('%d: ' % year, end='')
                    print('.', end='')
                    sys.stdout.flush()
