# coding=utf-8
import math
import random
from mat4py import loadmat
import numpy as np
import sys
import time

from sa import SimulatedAnnealing

cities = []


def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


def load_data(path):
    f = loadmat(path)
    for lat, log in zip(f['city']['lat'], f['city']['long']):
        # print("lat:%s, long:%s" % (lat, log))
        cities.append([lat, log])
    pass


def _convert_tuple(num):
    array = []
    for row in num:
        row = row.tolist()
        # print("row_0:", type(row[0]))
        array.append((row[0], row[1]))
    return array


def initial_solution():
    num = np.random.permutation(cities)
    print("type:", type(num))
    array = _convert_tuple(num)
    return array


def new_solution(x):
    x_new = x.copy()
    method = np.random.randint(2)
    if method == 0:
        np.random.shuffle(x_new)
    else:
        x_new = _convert_tuple(np.flip(x_new))
    return x_new


def new_solution2(x, method='reverse'):
    x_new = x.copy()
    city1 = math.ceil(random.random() * len(x))
    city2 = math.ceil(random.random() * len(x))
    # print("city1:%s, city2:%s, len:%s" % (city1, city2, len(x)))
    if method == 'reverse':
        min_ = min(city1, city2)
        max_ = max(city1, city2)
        if max_ < len(x):
            max_ = max_ + 1
        a = x[min_:max_]
        a.reverse()
        # print("min_:%s, max:%s, a:%s" % (min_, max_, a))
        """
        for i in range(min_):
            x_new[i] = x[i]
        for i in range(min_, max_):
            x_new[i] = a[i-min_]
        for i in range(max_, len(x)):
            x_new[i] = x[i]
        """
        x_new[:min_] = x[:min_]
        x_new[min_:max_] = a[0:max_ - min_]
        x_new[max_:] = x[max_:]
    else:
        x_new[min_] = x[max_]
        x_new[max_] = x[min_]

    return x_new


def weight_solution(array):
    d = distance(array[0], array[-1])
    for i in range(len(array) - 1):
        d += distance(array[i], array[i + 1])
    return d


if __name__ == "__main__":
    load_data("data/china.mat")
    n = initial_solution()
    k = 100
    print("n:", n)
    start = time.clock()
    sa = SimulatedAnnealing(initial=n, func=weight_solution, get=new_solution2, k=k, Tmax=1000)
    solutions, weight = sa.run()
    elapsed = time.clock() - start
    print(f"max solutions:{solutions}, weight:{weight}, elpased:{elapsed}")
    pass
    pass
