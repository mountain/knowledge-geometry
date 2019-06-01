# -*- coding: utf-8 -*-

import glob

from collections import Counter


for year in range(1600, 2000, 10):
    print('====================================================')
    print(year)
    print('----------------------------------------------------')
    freq_wrd = Counter()
    freq_ctx = Counter()
    wrd2ctx = {}

    for fname in glob.glob('./%ds/*.txt' % year):
        lns = open(fname, encoding='utf-8', errors='ignore').readlines()
        for ix, ln in enumerate(lns):
            if 500 < ix < len(lns) - 500:
                ln = ln.lower()
                ln = ln.replace('&', ' ').replace("\"", ' ').replace(":", ' ')
                ln = ln.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
                ln = ln[:-1].replace('_', '').replace('-', '').replace('|', '')
                ln = ln.replace('•', '').replace('◯', '')
                ln = ln.replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '')
                ln = ln.replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '')
                ln = ln.replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '')
                ln = ln.replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(';', '')
                ln = ln.replace('*', '').replace('+', '').replace('/', '').replace('~', '')
                ln = ln.replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
                wds = ln.rstrip().lstrip().split(' ')
                if len(wds) > 5:
                    for i in range(len(wds) - 4):
                        wnd = wds[i:i+5]
                        wrd = wnd[2]
                        ctx = '_'.join(sorted([
                            wnd[0], wnd[1],
                            wnd[3], wnd[4],
                        ]))
                        if wrd not in wrd2ctx:
                            wrd2ctx[wrd] = set()
                        wrd2ctx[wrd].add(ctx)

                        ctx = '%s_%s' % (wrd, ctx)
                        freq_wrd.update({wrd: 1})
                        freq_ctx.update({ctx: 1})

    print('----------------------------------------------------')
    with open('./%ds/freq.csv' % year, 'w+', encoding='utf-8') as o:
        for wrd, cnt in freq_wrd.most_common(10000):
            o.write('%d, %d, "%s"\n' % (cnt, len(wrd2ctx[wrd]), wrd))
    print('----------------------------------------------------')
    with open('./%ds/cntx.csv' % year, 'w+', encoding='utf-8') as o:
        for ctx, cnt in freq_ctx.most_common(30000):
            o.write('%d, "%s"\n' % (cnt, ctx))
    print('====================================================')
