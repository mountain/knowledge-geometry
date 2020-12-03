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
ax.set_ylim((-6 * 1.1, 6 * 1.1))

xs = np.ones([1], dtype=np.float128) + np.ones([1], dtype=np.float128) * 1.0j


def mk_cost(index):

    def cost(ratio):
        branch = arm[index]
        ys = branch * ratio
        a = xs.view(np.float128).reshape(1, 2)
        b = ys.view(np.float128).reshape(size, 2)
        return np.min(cdist(a, b, 'euclidean'))

    return cost


def loopscope(idx):
    if idx not in grid:
        return 4500, 4500, 1

    pos_start = grid[idx]['start']
    pos_end = grid[idx]['end']
    step = np.sign(pos_end - pos_start)
    if step > 0:
        pos_end = size
    elif step < 0:
        pos_end = 0
    else:
        step = 1
    return pos_start, pos_end, step


def trace0(central, branch):
    cursor = np.ones([1], dtype=np.float128) * 1.0j
    target = branch[np.argmin(np.abs(branch - cursor))]

    idx_start = size // 2
    r = np.abs(central - target)
    idx_end = np.argmin(r)
    if idx_start < idx_end:
        idx_step = 1
    else:
        idx_step = -1

    return trace(central, 1.0, '*', idx_start, idx_end, idx_step)


def trace(branch, assignment, op, idx_start, idx_end, idx_step):
    lastp, length = None, 0
    dist, lastdist, llastdist = None, None, None
    lastassignment = None
    for sx in range(idx_start, idx_end, idx_step):
        p = branch[sx]
        if lastp is not None:
            ds = np.sqrt((np.abs(p - lastp) ** 2) / (np.imag((p + lastp) / 2) ** 2))
            if op == '+':
                assignment = assignment + (ds / ratio * idx_step)
            if op == '*':
                assignment = assignment * np.exp(ds / ratio * idx_step)

        dist = np.abs(p - xs)
        #print('%s: %s, %s, %s' % (sx, p, dist, assignment))

        if lastdist is not None and llastdist is not None:
            if (dist - lastdist) * (lastdist - llastdist) < 0:
                break

        lastp = p
        llastdist = lastdist
        lastdist = dist
        lastassignment = assignment

    if op == '+':
        return lastassignment, '*'
    else:
        return lastassignment, '+'


for _ in range(arm.shape[0]):
    cost = mk_cost(_)
    res = minimize(cost, 1.0, method='Powell')
    scale = res.x
    branches = arm * scale
    center = branches.shape[0] // 2 - 1

    print('----------------------------------')
    print(scale)

    cursor = center
    while cursor != _:
        dirction = np.sign(_ - cursor)
        idx_start, idx_end, idx_step = loopscope(cursor + dirction)
        branch = branches[center + dirction]

        if cursor == center:
            assignment, op = trace0(arm[center], branch)
        assignment, op = trace(branch, assignment, op, idx_start, idx_end, idx_step)
        print('%s, %s: %s, %s' % (_, cursor, op, assignment))

        ps = branch[idx_start:idx_end:idx_step]
        ax.scatter(np.real(ps), np.imag(ps), s=1.0, c='red', marker='.')
        xx = np.max(np.real(ps))
        yx = np.max(np.imag(ps))
        wsize = max(xx, yx)
        ax.set_xlim((-wsize * 1.1, wsize * 1.1))
        ax.set_ylim((-wsize * 1.1, wsize * 1.1))
        adjust_aspect(fig, aspect=2)
        fig.savefig('trace%02d.png' % cursor)

        cursor += dirction

    print(assignment)