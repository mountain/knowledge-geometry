import numpy as np

from PIL import Image


width = 512
coord = np.linspace(-1, 1, num=width, dtype=np.complex128)
data = np.array([[x, y] for y in coord for x in coord]).reshape(width, width, 2)
colormap = np.array([
    [255, 255, 255, 0],
    [34, 139, 34, 255],
    [188, 143, 143, 255],
], dtype=np.uint8)


def reflect(ps, mir):
    return ps - 2 * np.sum(ps * mir, axis=-1, keepdims=True) * mir


def radius(ps):
    return np.sqrt(np.sum(ps * ps, axis=-1, keepdims=True))


def unify(ps):
    return ps / radius(ps)


def inner(a, b):
    return np.sum(a * b, axis=-1, keepdims=True)


def hbm2pdm(qs):  # hyperboloid model to poincare disk model
    return qs[:, :, 1:] / (1 + qs[:, :, 0])


def pdm2hbm(ps):  # poincare disk model to hyperboloid model
    rsq = np.sum(ps * ps, axis=2, keepdims=True)
    return np.concatenate([(1 + rsq) * 1j, 2 * ps[:, :, 0:1], 2 * ps[:, :, 1:2]], axis=2) / (1 - rsq)


def process(ps, mirror):
    u, v, w = mirror
    rs = np.zeros([width, width, 1], dtype=np.int)
    ts = np.zeros([width, width, 1], dtype=np.bool)
    for count in range(width // 16):
        for m in [u, v, w]:
            pos = inner(ps, m) > 0
            neg = np.logical_not(pos)
            rs = (rs + 1) * neg
            ts = ts | (rs >= 3) & (np.abs(inner(ps, u)) < 0.015)
            ps = reflect(ps, m) * pos + ps * neg
    return ts


def draw(mirror):
    disk = radius(data) < 1
    ps = pdm2hbm(data)
    ts = process(ps, mirror)
    return colormap[(2 * disk - ts) * disk][:, :, 0, :]


def calculate_mirror(p, q, r, t=(-10, -5, -1)):
    def refl(vector, mir):
        return vector - 2 * np.dot(vector, mir) * mir

    def unit(vector):
        magnitude = np.sqrt(np.abs(np.dot(vector, vector)))
        return vector / magnitude

    A, B, C = np.pi / np.array([p, q, r], dtype=np.float64)
    a = - np.cos(A)
    b = + np.sin(A)
    c = - np.cos(B)
    d = (- np.cos(C) - a * c) / b
    e = 1j * np.sqrt(np.abs(1 - c * c - d * d))
    mirror = np.array([
        [0, 1, 0],
        [0, a, b],
        [e, c, d]
    ], dtype=np.complex128)

    omni = unit(np.linalg.solve(mirror, np.array(t)))
    if omni[0].imag < 0:
        omni = - omni
    temp = unit(omni - np.array([1j, 0, 0]))

    for j, m in enumerate(mirror):
        target = refl(m, temp)
        if target[0].imag < 0:
            target = - target
        mirror[j] = target

    return mirror


def filename(p, q, r):
    a = str(int(p)) if p is not np.inf else 'i'
    b = str(int(q)) if q is not np.inf else 'i'
    c = str(int(r)) if r is not np.inf else 'i'
    return '%s%s%s.png' % (a, b, c)


if __name__ == '__main__':
    import time

    start = time.time()

    p, q, r = 2, 3, 8
    mirror = calculate_mirror(p, q, r)
    print(mirror)
    img = Image.fromarray(draw(mirror))
    img.save(filename(p, q, r))

    print("time:", time.time() - start)
