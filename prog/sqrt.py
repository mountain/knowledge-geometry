
def sqrt(val):
    dt = 1e-5
    cx, cy = 1 - (1 + val) / 2, 0.0
    x, y = - val, 0.0
    for i in range(int(val / dt)):
        dx, dy = x - cx, y - cy
        x += dy * dt
        y += -dx * dt
        if abs(x) < 1e-4:
            break
    return y


def sqrt_expr(val):
    cx, cy = 1 - (1 + val) / 2, 0.0
    x, y = - val, 0.0
    evl = val
    while abs(evl) > 1e-5:
        dx, dy = x - cx, y - cy
        x += dy / 1024
        y += - dx / 1024
        evl = evl + dy / 1024 - 0.6931471805599453 * evl * dx / 1024
        print(evl)
    return y


print(sqrt_expr(2))
