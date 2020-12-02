import numpy as np
import pickle
import gzip

from scipy.spatial.distance import cdist


iteration = 50
granularity = 180
size = iteration * granularity + 1

# 1.85501339 at iteration = 500 and granularity = 200
ratio = np.array([1.85501339 * np.pi], dtype=np.float128)


angles = np.linspace(0, np.pi, size, dtype=np.float128)
axis_m = np.zeros(size, dtype=np.float128) + np.linspace(0, size / 1000, size, dtype=np.float128) * 1j
axis_a0 = (np.cos(angles) + np.sin(angles) * 1j)


def mk_mobius(a, b, c, d):
    def mobius(w):
        return (a * w + b) / (c * w + d)
    def inverse(w):
        return (d * w - b) / (- c * w + a)
    return mobius, inverse


def mk_arm(arclength):
    axis_an1 = axis_a0 / arclength

    lastf = axis_an1
    lasti = axis_an1
    arm = [axis_a0, axis_m, axis_a0]
    fwd, inv = mk_mobius(1.0, -1.0, 1.0, +1.0)

    for _ in range(iteration):
        lastf = fwd(lastf)
        arm.append(lastf)
        lastf = lastf / arclength

    arm = list(reversed(arm))

    for _ in range(iteration):
        lasti = inv(lasti)
        arm.append(lasti)
        lasti = lasti / arclength

    return np.array(arm), fwd, inv


grid = {}
arm, fwd, inv = mk_arm(ratio)


def validate():
    kx = None
    for _ in range(2 * iteration):
        print('validating %s ...' % _)
        xs, ys = arm[_], arm[_ + 1]
        a = xs.view(np.float128).reshape(size, 2)
        b = ys.view(np.float128).reshape(size, 2)
        dm = cdist(a, b, 'euclidean')
        pos = np.argmin(dm)
        ix, jx = pos // size, pos % size
        d1 = dm[ix, jx]
        d2 = np.abs(xs[ix] - ys[jx])
        print('%s %s...' % (d1, d2))
        assert d1 - d2 < 0.0001 and d1 < 0.001
        k = np.real((xs[ix + 1] - xs[ix - 1]) / (ys[jx + 1] - ys[jx - 1]))
        print('%s ...' % k)
        assert k < 0.006
        if kx is not None:
            if kx > ix:
                step = -1
            else:
                step = +1
            lastp, length = None, 0
            for sx in range(kx, ix, step):
                p = xs[sx]
                if lastp is not None:
                    ds2 = (np.abs(p - lastp) ** 2) / (np.imag((p + lastp) / 2) ** 2)
                    length += np.sqrt(ds2)
                lastp = p
            print('%s: d(%s, %s) = %s ...' % (_, kx, ix, length))
            grid[_] = {'start': kx, 'end': ix, 'length': length}

        kx = jx


validate()

data = {
    'iteration': iteration,
    'granularity': granularity,
    'size': size,
    'ratio': ratio,
    'arm': arm,
    'grid': grid
}

with gzip.open('arm.pkl.gz', mode='wb') as g:
    pickle.dump(data, g)
