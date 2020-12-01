import numpy as np

import matplotlib.pyplot as plt

from scipy.spatial.distance import cdist

iteration = 100
size = 10000
ratio = 1.85523 * np.pi


fig, ax = plt.subplots()
fig.set_size_inches(74, 42, forward=True)


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


def mk_mobius(a, b, c, d):
    def mobius(w):
        return (a * w + b) / (c * w + d)
    def inverse(w):
        return (d * w - b) / (- c * w + a)
    return mobius, inverse


angles = np.linspace(0, np.pi, size, dtype=np.float128)
axis_m = np.zeros(size, dtype=np.float128) + np.linspace(0, size / 100, size, dtype=np.float128) * 1j
axis_an1 = (np.cos(angles) + np.sin(angles) * 1j) / ratio
axis_a0 = (np.cos(angles) + np.sin(angles) * 1j)
axis_ap1 = (np.cos(angles) + np.sin(angles) * 1j) * ratio

lastf = axis_an1
lasti = axis_an1
arm = [axis_a0, axis_m, axis_a0]
fwd, inv = mk_mobius(1.0, -1.0, 1.0, +1.0)

for _ in range(iteration):
    lastf = fwd(lastf)
    arm.append(lastf)
    lastf = lastf / ratio

arm = list(reversed(arm))

for _ in range(iteration):
    lasti = inv(lasti)
    arm.append(lasti)
    lasti = lasti / ratio

arm = np.array(arm)
ax.scatter(np.real(arm.flatten()), np.imag(arm.flatten()), s=0.1, c='blue', marker='.')
fig.savefig('arm.png')


def validate():
    kx = None
    for _ in range(2 * iteration + 2):
        print('validating %s ...' % _)
        xs, ys = arm[_], arm[_ + 1]
        a = xs.view(np.float64).reshape(size, 2)
        b = ys.view(np.float64).reshape(size, 2)
        dm = cdist(a, b, 'euclidean')
        pos = np.argmin(dm)
        ix, jx = pos // size, pos % size
        d1 = dm[ix, jx]
        d2 = np.abs(xs[ix] - ys[jx])
        print('%s ...' % d1)
        assert d1 == d2 and d1 < 0.001
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
            print('d(%s, %s) = %s ...' % (kx, ix, length))
        kx = jx


wsize = 1.0
for _ in range(1):
    arm1 = fwd(arm) # rotate right
    ax.scatter(np.real(arm1), np.imag(arm1), s=0.1, c='green', marker='.')
    arm2 = inv(arm) # rotate left
    ax.scatter(np.real(arm2), np.imag(arm2), s=0.1, c='red', marker='.')
    arm3 = arm * ratio # scale up
    ax.scatter(np.real(arm3), np.imag(arm3), s=0.1, c='yellow', marker='.')
    # arm4 = arm / ratio # scale down
    # ax.scatter(np.real(arm4), np.imag(arm4), s=0.1, c='green', marker='.')

    # arm5 = arm * np.sqrt(ratio) # scale up
    # ax.scatter(np.real(arm5), np.imag(arm5), s=0.1, c='blue', marker='.')
    # arm6 = arm / np.sqrt(ratio) # scale down
    # ax.scatter(np.real(arm6), np.imag(arm6), s=0.1, c='blue', marker='.')
    #
    # arm7 = arm * np.sqrt(np.sqrt(ratio)) # scale up
    # ax.scatter(np.real(arm7), np.imag(arm7), s=0.1, c='green', marker='.')
    # arm8 = arm * np.sqrt(np.sqrt(ratio)) * np.sqrt(ratio) # scale down
    # ax.scatter(np.real(arm8), np.imag(arm8), s=0.1, c='green', marker='.')

    wsize *= ratio
    ax.set_xlim((-wsize * 1.1, wsize * 1.1))
    ax.set_ylim((0, wsize * 1.1))
    adjustFigAspect(fig, aspect=2)
    fig.savefig('halfplane%s.png' % _)

    arm = np.concatenate([arm1, arm2, arm3])
