import numpy as np
import torch as th
import torch.nn as nn
import torch.nn.functional as fn


class Theta(nn.Module):
    def __init__(self):
        super(Theta, self).__init__()
        self.linear1 = nn.Linear(1, 8)
        self.linear2 = nn.Linear(8, 16)
        self.linear3 = nn.Linear(16, 8)
        self.linear4 = nn.Linear(8, 1)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, t):
        l1 = self.relu(self.linear1(t))
        l2 = self.relu(self.linear2(l1))
        l3 = self.relu(self.linear3(l2))
        return 2 * th.pi * fn.tanh(self.linear4(l3))


thetafn = Theta()


def loss(xfn, t0, tt, n):
    x0 = xfn(t0)
    ts = [t0]
    xs = [x0]
    epsilon = (tt - t0) / n

    t = t0
    x = xfn(x0)
    while t < tt:
        theta = thetafn(x)
        x = (1 + epsilon * th.sin(theta)) * x + epsilon * th.cos(theta)

        t += epsilon
        ts.append(t)
        xs.append(x)

    ta = th.DoubleTensor(ts)
    xa = th.DoubleTensor(xs)

    return th.mean((xa - xfn(ta)) * (xa - xfn(ta)))
