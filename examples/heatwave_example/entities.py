import collections
import threading

import numpy as np

from scenario.executor import queues_dictionary


class MeasurementVector():
    def __init__(self):
        self.vector = collections.namedtuple("TemperatureVector", ['temperature'])
        self.vector.temperature = 0


class World(object):
    def __init__(self):
        self.iteration_counter = 0
        self.length = 50
        self.width = 50
        self.space = [[MeasurementVector() for i in range(self.length)] for j in range(self.width)]

    def transformation(self):
        # heating device
        gr = np.eye(10) * 2000
        for iGr in range(10):
            gr[iGr, -iGr - 1] = 2000
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.space[i + 20][j + 10]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]
        for i in range(0, 10):
            for j in range(0, 10):
                point = self.space[i + 20][j + 30]
                if gr[i, j]:
                    point.vector.temperature = gr[i, j]

            for j in range(0, self.length):
                for i in range(0, self.width):
                    upper = None if j == self.length-1 else self.space[i][j + 1].vector.temperature
                    down = None if j == 0 else self.space[i][j - 1].vector.temperature
                    left = None if i == 0 else self.space[i - 1][j].vector.temperature
                    right = None if i == self.width-1 else self.space[i + 1][j].vector.temperature
                    elems = [y for y in filter(lambda x : x is not None, (upper, down, left, right))]
                    self.space[i][j].vector.temperature = sum(elems) / len(elems)

            # Re-assert heaters
            for i in range(0, 10):
                for j in range(0, 10):
                    point = self.space[i + 20][j + 10]
                    if gr[i, j]:
                        point.vector.temperature = gr[i, j]
            for i in range(0, 10):
                for j in range(0, 10):
                    point = self.space[i + 20][j + 30]
                    if gr[i, j]:
                        point.vector.temperature = gr[i, j]

    def start_time_transformation(self):
        #TODO: make world initialization
        self.transformation()
        self.update_rate = 0.5

        def transform_each_seconds():
            self.transformation()
            self.iteration_counter += 1
            queues_dictionary["iteration_completed"].put(1)
            threading.Timer(self.update_rate, transform_each_seconds).start()
        transform_each_seconds()