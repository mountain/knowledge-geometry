import numpy as np

import matplotlib.pyplot as plt


fig, ax = plt.subplots()


def adjustFigAspect(fig, aspect=1):
    '''
    Adjust the subplot parameters so that the figure has the correct
    aspect ratio.
    '''
    xsize, ysize = fig.get_size_inches()
    minsize = min(xsize, ysize)
    xlim = 0.7 * minsize/xsize
    ylim = 0.7 * minsize/ysize
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
ax.set_xlim((-3, 3))
ax.set_ylim((0, 3))


def mk_mobius(a, b, c, d):
    def mobius(w):
        return (a * w + b) / (c * w + d)
    return mobius


angles = np.linspace(0, np.pi, 100000)
axis_m = np.zeros(100000) + np.linspace(0, 1000, 100000) * 1j
axis_an1 = (np.cos(angles) + np.sin(angles) * 1j) / np.e
axis_a0 = (np.cos(angles) + np.sin(angles) * 1j)
axis_ap1 = (np.cos(angles) + np.sin(angles) * 1j) * np.e

ax.scatter(np.real(axis_m), np.imag(axis_m), s=0.1, c='blue', marker='.')
ax.scatter(np.real(axis_an1), np.imag(axis_an1), s=0.1, c='red', marker='.')
ax.scatter(np.real(axis_a0), np.imag(axis_a0), s=0.1, c='red', marker='.')
ax.scatter(np.real(axis_ap1), np.imag(axis_ap1), s=0.1, c='red', marker='.')

m = mk_mobius(1.0, 1.0, 1.0, -1.0)

rs = m(axis_a0)
ax.scatter(np.real(rs), np.imag(rs), s=0.1, c='yellow', marker='.')


adjustFigAspect(fig, aspect=2)

fig.savefig('halfplane.png')
