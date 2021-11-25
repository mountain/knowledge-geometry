import numpy as np


for idx in range(129):
    b3 = np.base_repr(idx, base=3)
    if len(b3) == 1:
        b3 = '0000%s' % b3
    if len(b3) == 2:
        b3 = '000%s' % b3
    if len(b3) == 3:
        b3 = '00%s' % b3
    if len(b3) == 4:
        b3 = '0%s' % b3
    print('%03d' % idx, b3, '%0.4f' % np.arcsinh(idx), np.binary_repr(np.int(np.arcsinh(idx) * 128), width=10))
