import numpy as np
import pickle
import gzip
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from scipy.spatial.distance import cdist


fig, ax = plt.subplots()
fig.set_size_inches(74, 42, forward=True)


with gzip.open('arm.pkl.gz', mode='rb') as g:
    data = pickle.load(g)
    iteration = data['iteration']
    granularity = data['granularity']
    size = data['size']
    ratio = data['ratio']
    arm = data['arm']
    grid = data['grid']


def mk_mobius(a, b, c, d):
    def mobius(w):
        return (a * w + b) / (c * w + d)
    def inverse(w):
        return (d * w - b) / (- c * w + a)
    return mobius, inverse


fwd, inv = mk_mobius(1.0, -1.0, 1.0, +1.0)


def adjust_aspect(fig, aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize, ysize = fig.get_size_inches()
    minsize = min(xsize, ysize)
    xlim = 0.9 * minsize/xsize
    ylim = 0.9 * minsize/ysize
    if aspect < 1:
        xlim *= aspect
    else:
        ylim /= aspect
    fig.subplots_adjust(left=0.5-xlim,
                        right=0.5+xlim,
                        bottom=0.5-ylim,
                        top=0.5+ylim)


ax.spines['left'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.set_xlim((-6 * 1.1, 6 * 1.1))
ax.set_ylim((0, 6 * 1.1))


xs = np.ones([1], dtype=np.float128) + np.ones([1], dtype=np.float128) * 1.0j


def mk_cost(index):

    def cost(ratio):
        branch = arm[index]
        ys = branch * ratio
        a = xs.view(np.float128).reshape(1, 2)
        b = ys.view(np.float128).reshape(size, 2)
        return np.min(cdist(a, b, 'euclidean'))

    return cost


for _ in range(arm.shape[0]):
    res = minimize(mk_cost(_), 1.0, method='Powell')
    scale = res.x
    print(scale)
    if scale[0] > 0:
        branch = arm[_] * scale
        assignment0 = np.exp(- np.log(scale) / np.log(ratio))



