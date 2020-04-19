# coding=utf-8
import math
import random

from sa import SimulatedAnnealing


def f_sin():
    lower = -4
    upper = 16
    initial = random.uniform(lower, upper)
    Tmax = 1000
    k = 100

    def func(x):
        return x * math.sin(x)

    def get(x):
        return (upper - lower) * random.random() + lower

    print("func 14:", func(14))
    sa = SimulatedAnnealing(initial=initial, func=func, get=get, k=k)
    solutions, weight = sa.run()
    print(f"min solutions:{solutions}, weight:{weight}")

    def func(x):
        return x * math.sin(x) * (-1)

    sa = SimulatedAnnealing(initial=initial, func=func, get=get, k=k)
    solutions, weight = sa.run()
    print(f"max solutions:{solutions}, weight:{weight}")
    pass


if __name__ == '__main__':
    f_sin()
