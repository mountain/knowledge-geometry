import numpy as np
import matplotlib

from sklearn.manifold import TSNE
from matplotlib import pyplot as plt

ix = 0
voc = []
voc2ix = {}
with open('vocabulary.txt') as v:
    for ln in v:
        voc.append(ln[:-1])
        voc2ix[ln[:-1]] = ix
        ix += 1


chdata = np.zeros([ix, ix])
wddata = np.zeros([ix, ix])
I = np.diag([1 for _ in range(ix)])

for i in range(ix):
    for j in range(ix):
        if voc[i][:2] == '模拟' and voc[j][:2] == '模拟':
            pass
        elif voc[i][-1] == '器' and voc[j][-1] == '器':
            pass
        elif voc[i][-2:] == '过程' and voc[j][-2:] == '过程':
            pass
        elif voc[i][-2:] == '系统' and voc[j][-2:] == '系统':
            pass
        else:
            if i != j:
                chdata[i, j] = len(set(voc[i]).intersection(set(voc[j]))) / np.sqrt(len(voc[i]) * len(voc[j]))


flow = []
with open('conceptflow.txt') as f:
    for ln in f:
        flow.append(ln[:-1])


wnd = 6
for ix, wd in enumerate(flow[wnd:-wnd]):
    if wd:
        i = voc2ix[wd]
        for order, ctx in enumerate(flow[ix:ix+wnd*2]):
            dist = 1 + np.abs(order - wnd)
            j = voc2ix[ctx]
            wddata[i, j] = wddata[i, j] + 1.5 / dist


wddata = wddata / wnd

print(chdata.min(), chdata.max(), chdata.mean())
print(wddata.min(), wddata.max(), wddata.mean())

data = np.sqrt(I + chdata + wddata + chdata * wddata)


tsne = TSNE(n_components=2, random_state=0)
proj = tsne.fit_transform(data)

matplotlib.use("pgf")
pgf_with_custom_preamble = {
    # "font.size": 18,
    "pgf.rcfonts": False,
    "text.usetex": True,
    "pgf.preamble": [
        # math setup:
        r"\usepackage{unicode-math}",

        # fonts setup:
        r"\setmainfont{Heiti SC}",
        r"\setsansfont{Heiti SC}",
        r"\setmonofont{Heiti SC}",
    ],
}
matplotlib.rcParams.update(pgf_with_custom_preamble)


matplotlib.rcParams['font.family'] = ['Heiti SC']
plt.figure(figsize=(20, 20))
for i in range(ix):
    if i < len(voc):
        plt.scatter(proj[i, 0], proj[i, 1])
        plt.annotate(voc[i], (proj[i, 0] + 0.1, proj[i, 1] + 0.1))
plt.savefig('concepts.png')
