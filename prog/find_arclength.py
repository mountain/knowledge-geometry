import numpy as np

from scipy.optimize import minimize


iteration = 500
granularity = 200
size = iteration * granularity + 1

# 1.85501339 at iteration = 500 and granularity = 200
arclength0 = np.array([1.85523 * np.pi], dtype=np.float128)


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


def cost(arclength):
    arm, fwd, inv = mk_arm(arclength)
    arm1 = fwd(arm) # rotate right
    arm2 = inv(arm) # rotate left

    error = np.abs(arm1[+0, +0] - arm[-1, 0]) ** 2 + np.abs(arm[+0, +0] - arm2[-1, 0]) ** 2
    print(error, np.real(arm1[+0, +0] - arm[-1, 0]), np.real(arm[+0, +0] - arm2[-1, 0]))

    return error


res = minimize(cost, arclength0, method='Powell')

print(res)
print(res.x / np.pi)
