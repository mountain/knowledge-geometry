# -*- coding: utf-8 -*-

import nltk
import matplotlib.pyplot as plt

from random import Random
from nltk.corpus import stopwords
from wordcloud import WordCloud
from matplotlib.cm import get_cmap

nltk.download('stopwords')
stopWords = set(stopwords.words('english') + [
    'one', 'two', 'first', 'every', 'de', 'mr', 'st',
    'would', 'could', 'shall', 'may', 'must', 'might',
    'never', 'even', 'also', 'yet', 'upon', 'without', 'though', 'through', 'back',
    'much', 'many', 'great', 'well', 'little', 'part',
    'us', 'thy', 'thou', 'another'])

wrd2frq = None
wrd2frq0 = {}
wrd2frq1 = {}
wrd2frq2 = {}
wrd2frq3 = {}
wrd2frq4 = {}

clrmap = {}
plasma = get_cmap('plasma')


def colorf(word, font_size, position, orientation, font_path, random_state):
    frq = wrd2frq[word]
    frqs = sorted([f for f in wrd2frq.values()], reverse=True)
    pos = frqs.index(frq)
    ratio = 255 - pos * 12
    c = tuple([int(255 * v) for v in plasma(ratio)])
    return c


for year in range(1600, 2000, 10):
    print('====================================================')
    print(year)
    print('----------------------------------------------------')

    if year % 50 == 0:
        wrd2frq4 = {}
    if year % 50 == 10:
        wrd2frq0 = {}
    if year % 50 == 20:
        wrd2frq1 = {}
    if year % 50 == 30:
        wrd2frq2 = {}
    if year % 50 == 40:
        wrd2frq3 = {}

    for ln in open('./%ds/freq.csv' % year, encoding='utf-8', errors='ignore'):
        freq, size, word = ln[:-1].split(',')
        word = word.strip()[1:-1]
        if word not in stopWords:

            if word not in wrd2frq0:
                wrd2frq0[word] = 0
            if word not in wrd2frq1:
                wrd2frq1[word] = 0
            if word not in wrd2frq2:
                wrd2frq2[word] = 0
            if word not in wrd2frq3:
                wrd2frq3[word] = 0
            if word not in wrd2frq4:
                wrd2frq4[word] = 0

            wrd2frq0[word] += float(freq)
            wrd2frq1[word] += float(freq)
            wrd2frq2[word] += float(freq)
            wrd2frq3[word] += float(freq)
            wrd2frq4[word] += float(freq)

    if year % 50 == 0:
        wrd2frq = wrd2frq0
    if year % 50 == 10:
        wrd2frq = wrd2frq1
    if year % 50 == 20:
        wrd2frq = wrd2frq2
    if year % 50 == 30:
        wrd2frq = wrd2frq3
    if year % 50 == 40:
        wrd2frq = wrd2frq4

    if year > 1640:
        cld = WordCloud(background_color="white", color_func=colorf,
                        max_words=20, width=1024, height=512, random_state=Random(47))
        cld.generate_from_frequencies(wrd2frq)

        plt.imshow(cld, interpolation='lanczos')
        plt.axis('off')
        plt.savefig('./wordcloud/%ds.png' % year)
