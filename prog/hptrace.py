import numpy as np
import pickle
import gzip

from scipy.optimize import minimize
from scipy.spatial.distance import cdist


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



def loopscope(idx):
    if idx not in grid:
        return 4500, 4500, 1

    pos_start = grid[idx]['start']
    pos_end = grid[idx]['end']
    step = np.sign(pos_end - pos_start)
    if step == 0:
        step = 1

    return pos_start, pos_end, step


def trace0(scale):
    return np.exp(scale), '+'


def tracez(xs, branch, assignment, op, idx_start, idx_end, idx_step):
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
        if lastdist is not None and llastdist is not None:
            if (dist - lastdist) * (lastdist - llastdist) < 0:
                break

        lastp = p
        llastdist = lastdist
        lastdist = dist
        lastassignment = assignment

    return lastassignment, lastdist


def trace(branch, assignment, op, idx_start, idx_end, idx_step):
    ps = branch[idx_start:idx_end:idx_step]
    ds = (np.abs(np.diff(ps)) ** 2) / (np.imag((ps[1:] + ps[:-1]) / 2) **2)
    if op == '+':
        delta = ds / ratio * idx_step
        assignment = assignment + np.sum(delta)
    if op == '*':
        delta = np.exp(ds / ratio * idx_step)
        assignment = assignment * np.prod(delta)

    if op == '+':
        return assignment, '*'
    else:
        return assignment, '+'


def verify_assignment(x, y):
    xs = x * np.ones([1], dtype=np.float128) + y * np.ones([1], dtype=np.float128) * 1.0j
    assert np.all(np.imag(xs) > 0)

    def mk_cost(index):

        def cost(ratio):
            branch = arm[index]
            ys = branch * ratio
            a = xs.view(np.float128).reshape(1, 2)
            b = ys.view(np.float128).reshape(size, 2)
            return np.min(cdist(a, b, 'euclidean'))

        return cost

    for _ in range(arm.shape[0]):
        cost = mk_cost(_)
        res = minimize(cost, np.ones([1], dtype=np.float64), method='Powell')
        scale = res.x
        if scale > 0 and res.fun < 1e-2:
            branches = arm * scale
            center = branches.shape[0] // 2 - 1

            index = center
            assignment, op = trace0(scale)
            dirction = np.sign(_ - index)
            while index != _:
                index += dirction
                branch = branches[index]
                idx_start, idx_end, idx_step = loopscope(index)
                assignment, op = trace(branch, assignment, op, idx_start, idx_end, idx_step)

            branch = branches[_]
            idx_start, idx_end, idx_step = loopscope(_)
            assignment, error = tracez(xs, branch, assignment, op, idx_start, idx_end, idx_step)

            if assignment is not None and error < 1e-2:
                print('----------------------------------')
                print(_, scale, assignment)


verify_assignment(-4.0, 1.1)
