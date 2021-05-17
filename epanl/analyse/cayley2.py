import numpy as np
import networkx as nx

curr2ij = {}
ij2curr = {}
edges = set()


for n in range(30):
    g = nx.Graph()
    w = 2 * n + 1
    for i in range(w):
        for j in range(w):
            g.add_node(i * w + j)

    for i in range(w - 1):
        for j in range(w - 1):
            curr = j * w + i
            upper = (j + 1) * w + i
            right = j * w + i + 1
            g.add_edge(curr, upper)
            g.add_edge(curr, right)

    j = w - 2
    for i in range(w):
        curr = j * w + i
        upper = (j + 1) * w + i
        g.add_edge(curr, upper)

    i = w - 2
    for j in range(w - 1):
        curr = j * w + i
        right = j * w + i + 1
        g.add_edge(curr, right)

    sptrm = nx.linalg.spectrum.laplacian_spectrum(g)
    print(n, w * w, sptrm.max())
