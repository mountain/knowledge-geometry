import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial.distance import cdist


fig, ax = plt.subplots()
fig.set_size_inches(74, 42, forward=True)


iteration = 50
granularity = 200
size = iteration * granularity + 1

# 1.85501339 at iteration = 500 and granularity = 200
arclength0 = np.array([1.85501339 * np.pi], dtype=np.float128)


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

steplength = {}


def adjustFigAspect(fig, aspect=1):
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


arm, fwd, inv = mk_arm(arclength0)


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
            steplength[_] = length

        kx = jx

validate()

print(len(steplength))

