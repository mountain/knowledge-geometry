import numpy as np


def validate(xfn, dxfn, thetafn, t0, tt, n):
    x0 = xfn(t0)
    ts = [t0]
    xs = [x0]
    epsilon = (tt - t0) / n

    t = t0
    x = xfn(x0)
    while t < tt:
        theta = thetafn(t, x)

        u = dxfn(t, x) / (np.cos(theta) + x * np.sin(theta))
        # x = x + u * epsilon * (np.cos(theta) + x * np.sin(theta))
        x = (1 + u * epsilon * np.sin(theta)) * x + u * epsilon * np.cos(theta)

        t += epsilon
        ts.append(t)
        xs.append(x)

    ta = np.array(ts)
    xa = np.array(xs)

    print(len(ts))
    print(np.mean((xa - xfn(ta)) * (xa - xfn(ta))))


print("validate square of t")
validate(lambda t: t * t, lambda t, x: 2 * t, lambda t, x: np.pi / 4, 0, 10, 10000)

print("validate cube of t")
validate(lambda t: t * t * t, lambda t, x: 3 * t * t, lambda t, x: np.pi / 4, 0, 10, 10000)

print("validate sine of t")
validate(lambda t: np.sin(t), lambda t, x: np.cos(t), lambda t, x: np.pi / 4, 0, 10, 10000)

print("validate cosine of t")
validate(lambda t: np.cos(t), lambda t, x: -np.sin(t), lambda t, x: np.arctan2(1, t), 0, 10, 10000)
