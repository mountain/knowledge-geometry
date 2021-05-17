import numpy as np
import networkx as nx


def visit(op, g, center, depth, max_depth):
    g.add_node(center)
    next = center + 1
    if depth > max_depth:
        return next
    else:
        if op != '-':
            g.add_edge(center, next)
            next = visit('+', g, next, depth + 1, max_depth)
        if op != '+':
            g.add_edge(center, next)
            next = visit('-', g, next, depth + 1, max_depth)
        if op != '/':
            g.add_edge(center, next)
            next = visit('*', g, next, depth + 1, max_depth)
        if op != '*':
            g.add_edge(center, next)
            next = visit('/', g, next, depth + 1, max_depth)
        return next


for ix in range(8):
    g = nx.Graph()
    ndcnt = visit('', g, 0, 0, ix)
    sptrm = nx.linalg.spectrum.laplacian_spectrum(g)
    print(ix, ndcnt, np.e ** 2, sptrm.max())
