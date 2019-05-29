# -*- coding: utf-8 -*-

import codecs

from pyquery import PyQuery as pq


chars = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
]

with codecs.open('works.txt', 'w', encoding='utf-8') as outa:
    for c in chars:
        d = pq(url='https://www.gutenberg.org/browse/authors/%s' % c)
        ac = d('div.pgdbbyauthor h2 a')
        uc = d('div.pgdbbyauthor ul')
        for ix, a in enumerate(ac):
            byear = -1
            dyear = -1
            name = ""
            status = 'ok'
            txta = pq(a).text()
            if len(txta) > 1:
                u = pq(uc[ix // 2])
                ls = u.find('li.pgdbetext')
                try:
                    sections = txta.split(',')
                    name = ', '.join(sections[:-1]).replace('  ', ' ').replace('  ', ' ')
                    assert('-' in sections[-1])
                    byear = int(sections[-1].split('-')[0])
                    dyear = int(sections[-1].split('-')[1])
                    aname = pq(a).attr("name")
                except Exception:
                    status = 'guess'
                    if byear != -1:
                        dyear = byear + 50
                if aname != 'a49712' and name != '' and 1580 < byear < 1980 and dyear != -1:
                    for l in ls:
                        txtt = pq(l).text()
                        anchor = pq(l).find('a')
                        title = pq(anchor).text()
                        code = pq(anchor).attr("href").split('/')[-1]
                        fields = txtt[len(title):].replace('(', '').replace(')', ',').split(',')
                        lang, form = fields[0].strip(), fields[1].strip()
                        ln = '%d\n%d\n%s\n%s\n%s\n%s\n%s\n%s\n' % (byear, dyear, status, lang, aname, name, form, code)
                        print(ln)
                        outa.write('%s\n' % ln)
                        outa.flush()

