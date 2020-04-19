# coding=utf-8
import math
import random


class SimulatedAnnealing(object):
    """
    """
    def __init__(self, **kwargs):
        self._initial_solutions = kwargs.pop('initial') or None
        self.T_max = kwargs.get('Tmax') or 1000
        self.T_min = kwargs.get('Tmin') or 1e-7
        self.K = kwargs.get('k') or 1000
        self.func = kwargs.pop('func')
        self.get = kwargs.pop('get')
        self.alpha = kwargs.get('alpha') or 0.98
        self.history_solutions = []
        self.history_weight = []
        self.max_stay_counter = kwargs.get('max_stay_counter') or self.K * 0.5
        self.best_solutions = self._initial_solutions
        self.best_weight = self.func(self.best_solutions)

    def cool_down(self, T):
        return T * self.alpha

    def is_close(self, a, b, rel_tol=1e-09, abs_tol=1e-30):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    def run(self):
        T = self.T_max
        current_solutions = self._initial_solutions
        while T > self.T_min or stay_counter > self.max_stay_counter:
            for i in range(self.K):
                current_weight = self.func(current_solutions)
                # generate new solution
                current = self.get(current_solutions)
                df = current_weight - self.func(current)
                # accept new solutions
                if df <= 0 or math.exp(-df / T) > random.random():
                    current_solutions = current
                    current_weight = self.func(current)
                    pass
                pass
                if current_weight < self.best_weight:
                    self.best_weight = current_weight
                    self.best_solutions = current_solutions

            T = self.cool_down(T)
            self.history_solutions.append(current_solutions)
            self.history_weight.append(current_weight)
            # print("solutions:%s, weight:%s, T:%s" % (current_solutions, current_weight, T))
            if len(self.history_solutions) >= 2 and self.is_close(self.history_solutions[-1], self.history_solutions[-2]):
                stay_counter += 1
            else:
                stay_counter = 0

        return self.best_solutions, self.best_weight
