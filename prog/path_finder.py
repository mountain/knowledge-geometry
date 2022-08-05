from fractions import Fraction

mu = 1
lmbd = 2
modulo = 8


def eval_path(path):
    result = 0
    for ix, op in enumerate(path):
        if ix % 2 == 0:
            result = (result + op) % modulo
        else:
            if op > 0:
                result = (result * op) % modulo
            else:
                result = result - (result // op) * op
                result = Fraction(result, -op)
    return result


def trace_path(path):
    ops = []
    result = []
    for ix, op in enumerate(path):
        ops.append(op)
        result.append(eval_path(ops))
    return result


def check_loop(path):
    val = eval_path(path)
    trace = trace_path(path)
    return len(path) > 1 and val in trace


def gen_traces(traces):
    result, flag = [], False
    for trace in traces:
        if check_loop(trace):
            result.append(trace)
        else:
            flag = True
            if len(trace) % 2 == 0:
                for adder in [-mu, 0, mu]:
                    result.append(trace + [adder])
            else:
                for multier in [-lmbd, 1, lmbd]:
                    result.append(trace + [multier])
    if not flag:
        return result
    else:
        return gen_traces(result)


for base in range(0, modulo):
    for trace in gen_traces([[base]]):
        loop = [eval_path(trace[:ix]) for ix in range(len(trace))]
        print(base, loop)
