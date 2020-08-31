import numpy as np


def func(x):
    return 2 * np.exp(x)


def derivative(f, x):
    delta = 0.01
    for _ in range(30):
        delta = delta / 2.0
        xp = x + delta
        y = f(x)
        yp = f(xp)
        u = np.exp(x)
        up = np.exp(xp)

        d1y = (yp - y) / (xp - x)
        d1u = (up - u) / (xp - x)
        d2y = np.log(d1y / d1u)

        print(1, x, y, d1y)
        print(1, x, y, d2y)


derivative(func, 2.0)