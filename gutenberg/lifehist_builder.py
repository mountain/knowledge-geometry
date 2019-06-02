# -*- coding: utf-8 -*-

import numpy as np
import nltk
import matplotlib.pyplot as plt

from collections import Counter
from nltk.corpus import stopwords


nltk.download('stopwords')
stopWords = set(stopwords.words('english'))

years = {}
sizes = {}
freqs = {}

wrd2frq0 = Counter()
wrd2frq1 = Counter()
wrd2frq2 = Counter()
wrd2frq3 = Counter()
wrd2frq4 = Counter()

cntx0 = Counter()
cntx1 = Counter()
cntx2 = Counter()
cntx3 = Counter()
cntx4 = Counter()

for year in range(1600, 2000, 10):
    print('====================================================')
    print(year)
    print('----------------------------------------------------')

    if year % 50 == 0:
        wrd2frq4 = Counter()
        cntx4 = Counter()
    if year % 50 == 10:
        wrd2frq0 = Counter()
        cntx0 = Counter()
    if year % 50 == 20:
        wrd2frq1 = Counter()
        cntx1 = Counter()
    if year % 50 == 30:
        wrd2frq2 = Counter()
        cntx2 = Counter()
    if year % 50 == 40:
        wrd2frq3 = Counter()
        cntx3 = Counter()

    ffreq = open('./%ds/freq.csv' % year, encoding='utf-8', errors='ignore')
    for ln in ffreq:
        freq, size, word = ln[:-1].split(',')
        word = word.strip()[1:-1]
        wrd2frq0.update({word: float(freq)})
        wrd2frq1.update({word: float(freq)})
        wrd2frq2.update({word: float(freq)})
        wrd2frq3.update({word: float(freq)})
        wrd2frq4.update({word: float(freq)})
    ffreq.close()

    fcntx = open('./%ds/cntx.csv' % year, encoding='utf-8', errors='ignore')
    for ln in fcntx:
        freq, cntx = ln[:-1].split(',')
        word = cntx.strip()[1:-1].split('_')[0]
        cntx0.update({word: float(freq)})
        cntx1.update({word: float(freq)})
        cntx2.update({word: float(freq)})
        cntx3.update({word: float(freq)})
        cntx4.update({word: float(freq)})
    fcntx.close()

    words = None
    if year > 1640:
        if year % 50 == 0:
            wrd2frq = wrd2frq0
            cntx = cntx0
        if year % 50 == 10:
            wrd2frq = wrd2frq1
            cntx = cntx1
        if year % 50 == 20:
            wrd2frq = wrd2frq2
            cntx = cntx2
        if year % 50 == 30:
            wrd2frq = wrd2frq3
            cntx = cntx3
        if year % 50 == 40:
            wrd2frq = wrd2frq4
            cntx = cntx4

        totalfq = np.sum([v for v in wrd2frq.values()])
        totalcx = np.sum([v for v in cntx.values()])
        words = wrd2frq.most_common(len(stopWords) + 10)
        for wd, fq in words:
            if wd not in stopWords:
                if wd not in years:
                    years[wd] = []
                years[wd].append(year)
                if wd not in sizes:
                    sizes[wd] = []
                sizes[wd].append(np.log10(cntx[wd] / totalcx))
                if wd not in freqs:
                    freqs[wd] = []
                freqs[wd].append(np.log10(fq / totalfq))

print(years.keys())

g1 = ['god']
g2 = ['one']
g3 = ['said']
g4 = ['would']

plt.figure(1)
for wd in g1:
    plt.subplot(411)
    plt.plot(years[wd], freqs[wd])
for wd in g2:
    plt.subplot(412)
    plt.plot(years[wd], freqs[wd])
for wd in g3:
    plt.subplot(413)
    plt.plot(years[wd], freqs[wd])
for wd in g4:
    plt.subplot(414)
    plt.plot(years[wd], freqs[wd])

plt.savefig('./wordcloud/trend.png')
plt.close()
