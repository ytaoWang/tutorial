# coding=utf-8
import math
import random
from mat4py import loadmat
import numpy as np
import sys
import time
import copy
from sa import SimulatedAnnealing

cities = []

data = {
    'New York City': (40.72, 74.00),
    'Los Angeles': (34.05, 118.25),
    'Chicago': (41.88, 87.63),
    'Houston': (29.77, 95.38),
    'Phoenix': (33.45, 112.07),
    'Philadelphia': (39.95, 75.17),
    'San Antonio': (29.53, 98.47),
    'Dallas': (32.78, 96.80),
    'San Diego': (32.78, 117.15),
    'San Jose': (37.30, 121.87),
    'Detroit': (42.33, 83.05),
    'San Francisco': (37.78, 122.42),
    'Jacksonville': (30.32, 81.70),
    'Indianapolis': (39.78, 86.15),
    'Austin': (30.27, 97.77),
    'Columbus': (39.98, 82.98),
    'Fort Worth': (32.75, 97.33),
    'Charlotte': (35.23, 80.85),
    'Memphis': (35.12, 89.97),
    'Baltimore': (39.28, 76.62)
}


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


def load_data2():
    for _, value in data.items():
        cities.append(value)


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


def initial_solution2():
    x = cities[:]
    random.shuffle(x)
    return x


def new_solution(x):
    x_new = x[:]
    method = np.random.randint(2)
    if method == 0:
        np.random.shuffle(x_new)
    else:
        x_new = _convert_tuple(np.flip(x_new))
    return x_new


def new_solution2(x, method='reverse'):
    x_new = copy.deepcopy(x)
    city1 = math.ceil(random.random() * len(x))
    city2 = math.ceil(random.random() * len(x))
    r = random.randint(0, 1)
    if r == 0:
        method = 'swap'
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
        city1 = city1 if city1 < len(x_new) else city1 - 1
        city2 = city2 if city2 < len(x_new) else city2 - 1
        x_new[city1], x_new[city2] = x_new[city2], x_new[city1]

    return x_new


def new_solution3(x, method='reverse'):
    city1 = random.randint(0, len(x) - 1)
    city2 = random.randint(0, len(x) - 1)
    x_new = x[:]
    x_new[city1], x_new[city2] = x_new[city2], x_new[city1]
    return x_new


def weight_solution(array):
    d = distance(array[0], array[-1])
    for i in range(len(array) - 1):
        d += distance(array[i], array[i + 1])
    return d


if __name__ == "__main__":
    # load_data("data/china.mat")
    load_data2()
    n = initial_solution2()
    k = 100
    print("n:", n)
    start = time.clock()
    sa = SimulatedAnnealing(initial=n, func=weight_solution, get=new_solution2, k=k, Tmax=1000)
    solutions, weight = sa.run()
    elapsed = time.clock() - start
    print(f"max solutions:{solutions}, weight:{weight}, elpased:{elapsed}")
    s = set(solutions)
    print("fronzen:%s, len:%s, solutions length:%s" % (s, len(s), len(solutions)))
    pass
    pass
