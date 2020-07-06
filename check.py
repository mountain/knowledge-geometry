import numpy as np

e = np.e
gamma = np.array([0.57721566490153286060651209008240243104215933593992], dtype=np.float128)[0] / 1.7616

elm_0 = 1
elm_1 = gamma
sum_inf = elm_0 + elm_1 / (1.0 - gamma)

sum, prd = 0, 1
for i in range(10000):
    if i == 0:
        elm = elm_0
    elif i == 1:
        elm = elm_1
    else:
        elm = elm * gamma
    sum = sum + elm
    res = (1 + sum_inf - sum)
    prd = prd * res
    print(elm, sum, res, prd)
