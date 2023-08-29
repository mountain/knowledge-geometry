from itertools import product

def solve(num, cache={0: ['ι']}):
    if num not in cache:
        cache[num] = ['(%s %s)' % t for i in range(1, num + 1)
            for t in product(solve(i - 1), solve(num - i))]
    return cache[num]

# Test
idx = 1
for num in range(0, 8):
    print(num)
    for s in solve(num):
        print('%03d' % idx, s)
        idx += 1
