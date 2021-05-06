import numpy as np
import networkx as nx
import matplotlib

from matplotlib import pyplot as plt

ix = 0
voc = []
voc2ix = {}
ix2voc = {}
with open('vocabulary.txt') as v:
    for ln in v:
        voc.append(ln[:-1])
        voc2ix[ln[:-1]] = ix
        ix2voc[ix] = ln[:-1]
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

num = data.shape[0]
g = nx.Graph()
for ix in range(num):
    g.add_node(ix)
for ix in range(num):
    for jx in range(num):
        g.add_edge(ix, jx, weight=data[ix, jx])


def color(ix):
    wd = ix2voc[ix]
    if '语' in wd:
        return 'green'
    if '形' in wd:
        return 'yellow'
    if '因' in wd:
        return 'red'
    if '物' in wd:
        return 'pink'
    if '算' in wd:
        return 'purple'
    if '理' in wd:
        return 'cyan'
    if '蕴' in wd:
        return 'gray'
    return 'blue'


cbc = nx.communicability_betweenness_centrality(g)


def size(ix):
    return np.sqrt(cbc[ix]) * 144000


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

pos = nx.spring_layout(g, weight='weight', k=0.4, iterations=100)
nx.draw_networkx(g, pos, labels={}, edgelist=[], node_color=list(map(color, g.nodes())), node_size=list(map(size, g.nodes())), alpha=0.2)
nx.draw_networkx(g, pos, labels=ix2voc, edgelist=[], node_size=0)
plt.savefig('network.png')
